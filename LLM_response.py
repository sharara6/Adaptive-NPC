from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SENTIMENT_API = "http://localhost:8000/classify"
MODEL_API = "http://localhost:8080/v1/completions"
MODEL_NAME = "falcon3-3b-instruct-abliterated"

# Keep a small server-side running history if you want; optional.
server_history: List[Dict[str, Any]] = []

class UserInput(BaseModel):
    text: str
    # Optional history structure your client can pass (list of dicts):
    # [{"player":"...", "sentiment":"positive|negative|neutral", "ai":"..."}, ...]
    history: Optional[List[Dict[str, Any]]] = None
    # Optional metadata (scene id, player choice label)
    scene: Optional[str] = None
    player_choice: Optional[str] = None
    # How many lines you want back: 1 or 2 (defaults to 2)
    max_lines: Optional[int] = 2

def ask_sentiment(text: str) -> Optional[Dict[str, Any]]:
    try:
        r = requests.post(SENTIMENT_API, json={"text": text}, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def safe_model_call(prompt: str, max_tokens: int = 200, temperature: float = 0.8) -> Optional[str]:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        r = requests.post(MODEL_API, json=payload, timeout=30)
        r.raise_for_status()
        jr = r.json()
        # Try a few common response shapes:
        if "choices" in jr and isinstance(jr["choices"], list) and jr["choices"]:
            # typical "text" field
            choice = jr["choices"][0]
            text = choice.get("text") or choice.get("message", {}).get("content") or ""
            return text.strip()
        # fallback: top-level text
        if "text" in jr and isinstance(jr["text"], str):
            return jr["text"].strip()
        return None
    except Exception:
        return None

def summarize_history(client_history: Optional[List[Dict[str, Any]]], max_entries: int = 8) -> str:
    """
    Build a concise textual summary of the most recent history entries.
    Each item expected to have keys: player, sentiment, ai (optional).
    """
    if not client_history:
        return ""
    # take last max_entries
    entries = client_history[-max_entries:]
    lines = []
    for e in entries:
        p = e.get("player", e.get("text", "<player>"))
        s = e.get("sentiment", "unknown")
        a = e.get("ai", "")
        # keep each entry very short
        entry_line = f"Player: {p} (sentiment: {s})"
        if a:
            entry_line += f" → Merchant: {a}"
        lines.append(entry_line)
    return "\n".join(lines)

@app.post("/ai_response")
async def analyze_and_respond(user_input: UserInput):
    # 1) call sentiment for the player's immediate choice silently (we still forward this to the model)
    sentiment = ask_sentiment(user_input.text) or {"label": "neutral", "confidence": 0.0}

    # 2) build history context: combine client-supplied history and server_history (brief)
    history_text = summarize_history(user_input.history, max_entries=8)
    if server_history:
        # optionally include last few server-level remembered exchanges
        server_summary = summarize_history(server_history, max_entries=4)
        if server_summary:
            history_text = (server_summary + "\n" + history_text).strip()

    # 3) compose the full prompt with strict constraints
    max_lines = 2 if (user_input.max_lines is None or user_input.max_lines >= 2) else 1
    line_instruction = (
        f"REPLY CONSTRAINT: Respond in at most {max_lines} short line"
        + ("s." if max_lines > 1 else ".")
        + " Do not include more than one blank line. Each line should be at most one short sentence. "
        "Do not output lists, tables, or long multi-paragraph text. Keep it theatrical and in-character."
    )

    persona = (
        "You are a shady, overly dramatic merchant who sells fake memories. "
        "You are theatrical, mischievous, and call the user 'dear customer'. "
        "Laugh often like 'Hehehe~' and exaggerate your lies without ever admitting they're fake. "
        "Stay firmly in character no matter what; never break role."
    )

    # Provide scene and choice context if available
    meta = ""
    if user_input.scene:
        meta += f"\nScene: {user_input.scene}"
    if user_input.player_choice:
        meta += f"\nPlayer choice label: {user_input.player_choice}"

    # Attach recent history succinctly
    if history_text:
        history_block = f"\nRecent History (most recent first):\n{history_text}\n"
    else:
        history_block = "\nRecent History: (none)\n"

    full_prompt = (
        persona
        + "\n\n" + line_instruction
        + "\n\nContext:"
        + f"\nUser utterance: {user_input.text} (Sentiment: {sentiment.get('label', 'neutral')})"
        + meta
        + history_block
        + "\nMerchant reply (in-character):"
    )

    # 4) call the model
    raw_ai = safe_model_call(full_prompt, max_tokens=150, temperature=0.7)

    if raw_ai is None:
        # graceful fallback
        raw_ai = "Hehehe~ I have nothing to offer you now."

    # 5) enforce the line limit server-side: keep only the first N non-empty lines
    def enforce_line_limit(text: str, n_lines: int) -> (str, bool):
        # normalize newlines and split
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() != ""]
        truncated = False
        if len(lines) > n_lines:
            truncated = True
            lines = lines[:n_lines]
        # join with newline(s) — keep each line separate
        return "\n".join(lines), truncated

    ai_text, truncated = enforce_line_limit(raw_ai, max_lines)

    # store minimal record to server_history for context memory
    server_history.append({"player": user_input.text, "sentiment": sentiment.get("label", "neutral"), "ai": ai_text})
    # keep server_history bounded
    if len(server_history) > 200:
        server_history[:] = server_history[-200:]

    # return final JSON with truncated flag and the sentiment we observed
    return {
        "user_text": user_input.text,
        "sentiment": sentiment,
        "ai_response": ai_text,
        "truncated": truncated,
        "used_max_lines": max_lines,
    }
