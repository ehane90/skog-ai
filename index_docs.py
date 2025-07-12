import os
import faiss
import openai
import numpy as np
from PyPDF2 import PdfReader
from openai.embeddings_utils import get_embedding
import pickle
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_pdfs(folder):
    texts, files = [], []
    for f in os.listdir(folder):
        if f.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder, f))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            texts.append(text)
            files.append(f)
    return texts, files

def chunk_text(text, size=500):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

texts, files = read_pdfs("docs")
chunks, sources = [], []

for text, filename in zip(texts, files):
    for chunk in chunk_text(text):
        chunks.append(chunk)
        sources.append(filename)

embeddings = [get_embedding(c, model="text-embedding-3-small") for c in chunks]
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings).astype("float32"))

with open("data.pkl", "wb") as f:
    pickle.dump((index, chunks, sources), f)
