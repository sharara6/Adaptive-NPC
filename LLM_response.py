from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # ← ADD THIS
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

class UserInput(BaseModel):
    text: str

MODEL_API = "http://localhost:8080/v1/completions"
MODEL_NAME = "falcon3-3b-instruct-abliterated"

history = ""

@app.post("/ai_response")
async def analyze_and_respond(user_input: UserInput):
    global history
    sentiment_response = requests.post(SENTIMENT_API, json={"text": user_input.text})
    sentiment = sentiment_response.json()

    full_prompt = history + f"\nUser: {user_input.text} (Sentiment: {sentiment['label']})\nAI:"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "max_tokens": 200,
    }
    model_response = requests.post(MODEL_API, json=payload)
    ai_text = model_response.json()["choices"][0]["text"].strip()
    print(f"User said: {user_input.text}")
    print(f"Sentiment: {sentiment['label']}")
    print(f"AI response: {ai_text}")
    history += f"\nUser: {user_input.text} (Sentiment: {sentiment['label']})\nAI: {ai_text}"

    return {
        "user_text": user_input.text,
        "sentiment": sentiment,
        "ai_response": ai_text
    }
