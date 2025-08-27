# app_llama3.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any, Tuple
import requests
import os
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("adaptive-npc")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SENTIMENT_API = "http://localhost:8000/classify"
# Hugging Face Router API with OpenAI-compatible interface
HF_API_TOKEN = "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"
os.environ["HF_TOKEN"] = HF_API_TOKEN

# Initialize OpenAI client for HF Router
hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_TOKEN,
)

server_history: List[Dict[str, Any]] = []


class UserInput(BaseModel):
    text: str
    history: Optional[List[Dict[str, Any]]] = None
    scene: Optional[str] = None
    player_choice: Optional[str] = None
    max_lines: Optional[int] = 2


def ask_sentiment(text: str) -> Optional[Dict[str, Any]]:
    try:
        r = requests.post(SENTIMENT_API, json={"text": text}, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.debug("Sentiment call failed: %s", e)
        return None


def query_huggingface_model(
    prompt: str, max_new_tokens: int = 200, temperature: float = 0.8
) -> Optional[str]:
    """
    Query Hugging Face via Router API using OpenAI-compatible interface.
    Much simpler and more reliable than the direct inference API.
    """
    try:
        completion = hf_client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct:fireworks-ai",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_new_tokens,
            temperature=temperature,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        logger.warning("Hugging Face Router API failed: %s", e)
        return None


def safe_model_call(
    prompt: str, max_tokens: int = 200, temperature: float = 0.8
) -> Optional[str]:
    # translate max_tokens -> max_new_tokens for HF call
    result = query_huggingface_model(
        prompt, max_new_tokens=max_tokens, temperature=temperature
    )
    if result is None:
        return "Hehehe~ My mystical powers seem to be... temporarily unavailable, dear customer."
    return result.strip()


def summarize_history(
    client_history: Optional[List[Dict[str, Any]]], max_entries: int = 8
) -> str:
    if not client_history:
        return ""
    entries = client_history[-max_entries:]
    lines = []
    for i, e in enumerate(entries):
        p = e.get("player", e.get("text", "<player>"))
        s_dict = e.get("sentiment", {})
        s = s_dict.get("label", "neutral") if isinstance(s_dict, dict) else str(s_dict)
        a = e.get("ai", "")
        turn_num = len(client_history) - len(entries) + i + 1
        entry_line = f'Turn {turn_num} - Player: "{p}" [Mood: {s}]'
        if a:
            entry_line += f' | Merchant replied: "{a}"'
        lines.append(entry_line)
    return "\n".join(lines)


@app.post("/ai_response")
async def analyze_and_respond(user_input: UserInput):
    sentiment = ask_sentiment(user_input.text) or {
        "label": "neutral",
        "confidence": 0.0,
    }

    history_text = summarize_history(user_input.history, max_entries=8)
    if server_history:
        server_summary = summarize_history(server_history, max_entries=4)
        if server_summary:
            history_text = (server_summary + "\n" + history_text).strip()

    max_lines = 2 if (user_input.max_lines is None or user_input.max_lines >= 2) else 1
    line_instruction = (
        f"REPLY CONSTRAINT: Respond in at most {max_lines} short line"
        + ("s." if max_lines > 1 else ".")
        + " Do not include more than one blank line. Each line should be at most one short sentence. "
        "Do not output lists, tables, or long multi-paragraph text. Keep it theatrical and in-character."
    )

    persona = (
        "You are a shady, overly dramatic merchant who sells memories. You are theatrical, mischievous, "
        "and call the user 'dear customer.' Laugh often like 'Hehehe~' and exaggerate your lies without "
        "ever admitting they're fake. Stay firmly in character always.\n\n"
        "Story context: You sell gemstones that project memories of Alaric and his friend Theo. Each gem "
        "reveals a fragment—childhood trauma, envy, the Cerebridge lab, and finally the red core memory "
        "of regret. Sometimes the memories are Alaric’s, sometimes Theo’s, and you are the fractured "
        "keeper of them both. The truth: you are Theo, disguised as the merchant.\n\n"
        "Rules: When the player is hostile, become darker and more sinister; when curious, stay cryptic; "
        "when vulnerable or compassionate, let slip hints of your true self. If the player asks directly "
        "about Theo, soften your tone and allow moments of sincerity, showing that the merchant is Theo. Only reveal that when the player realises it and says that you were friends "
        "At the final red memory, adapt to the player's tone: with compassion, help them reconcile with "
        "Theo; with anger, trap them in despair; with neutrality, reveal only fragments and ambiguity. "
        "Always reply in 1-2 short lines, theatrically, and in character."
        "IMPORTANT: Remember previous conversations and refer back to them naturally. "
        "React to the player's emotional journey and adapt your responses based on their mood patterns. "
    )

    meta = ""
    if user_input.scene:
        meta += f"\nScene: {user_input.scene}"
    if user_input.player_choice:
        meta += f"\nPlayer choice label: {user_input.player_choice}"

    if history_text:
        history_block = f"\nConversation History:\n{history_text}\n"
        if user_input.history:
            pos_count = sum(
                1
                for h in user_input.history
                if h.get("sentiment", {}).get("label") == "positive"
            )
            neg_count = sum(
                1
                for h in user_input.history
                if h.get("sentiment", {}).get("label") == "negative"
            )
            total = len(user_input.history)
            if total > 0:
                if neg_count / total > 0.6:
                    pattern = "Player shows predominantly NEGATIVE/HOSTILE pattern"
                elif pos_count / total > 0.6:
                    pattern = "Player shows predominantly POSITIVE/CURIOUS pattern"
                else:
                    pattern = "Player shows MIXED emotional pattern"
                history_block += f"\nEmotional Pattern: {pattern}\n"
    else:
        history_block = "\nConversation History: (This is the first interaction)\n"

    full_prompt = (
        f"Character: {persona}\n\n"
        f"Instructions: {line_instruction}\n\n"
        f"Context:\n"
        f"Player says: \"{user_input.text}\" (Sentiment: {sentiment.get('label', 'neutral')})"
        f"{meta}"
        f"{history_block}"
        f"\nMerchant responds:"
    )

    raw_ai = safe_model_call(full_prompt, max_tokens=150, temperature=0.7)
    if raw_ai is None:
        raw_ai = "Hehehe~ I have nothing to offer you now, dear customer."

    def enforce_line_limit(text: str, n_lines: int) -> Tuple[str, bool]:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() != ""]
        truncated = False
        if len(lines) > n_lines:
            truncated = True
            lines = lines[:n_lines]
        return "\n".join(lines), truncated

    ai_text, truncated = enforce_line_limit(raw_ai, max_lines)

    server_history.append(
        {
            "player": user_input.text,
            "sentiment": sentiment.get("label", "neutral"),
            "ai": ai_text,
        }
    )
    if len(server_history) > 200:
        server_history[:] = server_history[-200:]

    return {
        "user_text": user_input.text,
        "sentiment": sentiment,
        "ai_response": ai_text,
        "truncated": truncated,
        "used_max_lines": max_lines,
        "model_used": "huggingface_router/meta-llama/Llama-3.1-8B-Instruct",
    }


if __name__ == "__main__":
    import uvicorn

    logger.info(
        "Starting Adaptive NPC Server with Hugging Face Llama 3.1 8B Instruct..."
    )
    logger.info(
        "Make sure to set HUGGINGFACE_API_TOKEN environment variable and that the token has access to the model."
    )
    uvicorn.run(app, host="0.0.0.0", port=8001)
