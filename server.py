"""
@inproceedings{barbieri-etal-2020-tweeteval,
    title = "{T}weet{E}val: Unified Benchmark and Comparative Evaluation for Tweet Classification",
    author = "Barbieri, Francesco  and
      Camacho-Collados, Jose  and
      Espinosa Anke, Luis  and
      Neves, Leonardo",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.findings-emnlp.148",
    doi = "10.18653/v1/2020.findings-emnlp.148",
    pages = "1644--1650"
}
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax
import numpy as np
import torch

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
labels = ["negative", "neutral", "positive"]

@app.post("/classify")
async def classify(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text.strip():
        return {"label": "neutral", "confidence": 0.0}
    encoded = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**encoded)
    scores = softmax(output.logits[0].numpy())
    max_idx = np.argmax(scores)
    return {
        "label": labels[max_idx],
        "confidence": round(float(scores[max_idx]), 4)
    }
