from typing import List
import json
import os
from io import BytesIO

import httpx
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from docx import Document
import PyPDF2

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num] 
        text += page.extract_text()
    return text

def read_docx(file):
    doc = Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def embedding(texts: List[str]):
    url = "https://api-inference.huggingface.co/models/maidalun1020/bce-embedding-base_v1"
    if not os.getenv("HF_API_KEY"):
        raise ValueError("Please set the HF_API_KEY environment variable")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("HF_API_KEY")}'
    }
    payload = json.dumps({
    "inputs": texts
    })
    response = httpx.request("POST", url, headers=headers, data=payload)
    return response.json(), response.status_code

def calculate_similarity(vectors: List[str]):
    vectors = np.array(vectors)
    similarity = cosine_similarity(vectors)
    score = round(similarity[0][1], 2)
    return score