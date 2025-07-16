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
"""This Was created for Testing Purposes"""

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
import os
import shutil



# Check if the model directory exists
MODEL_DIR = "cardiffnlp/twitter-roberta-base-sentiment"
if os.path.exists(MODEL_DIR):
    print(f"Model directory '{MODEL_DIR}' exists. Deleting it...")
    shutil.rmtree(MODEL_DIR)
    print(f"Deleted '{MODEL_DIR}'")

# Tasks:

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

# download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]



# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)

def classify_text_choice(text):
    """
    Classify text into one of three choices: positive, negative, or neutral
    Returns: (choice, confidence_score)
    """
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    # Get the highest scoring label
    max_index = np.argmax(scores)
    choice = labels[max_index]
    confidence = float(scores[max_index])
    
    return choice, confidence

# Example usage for testing
text = "Good night 😊"
choice, confidence = classify_text_choice(text)
print(f"Text: '{text}'")
print(f"Classification: {choice}")
print(f"Confidence: {np.round(confidence, 4)}")


