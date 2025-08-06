import os
import pickle
import faiss
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

# 🔐 Ladda OpenAI-nyckel
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Embedding-funktion
def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# 📄 Läs dokument
def read_documents(folder="docs"):
    texts, sources = [], []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        print(f"📥 Läser in: {filename}")
        text = ""

        if filename.endswith(".pdf"):
            with open(path, "rb") as f:
                reader = PdfReader(f)
                text = "\n".join([p.extract_text() or "" for p in reader.pages])

        elif filename.endswith(".docx"):
            doc = Document(path)
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(path, sheet_name=None)
            for sheet, sheet_df in df.items():
                text += f"\n\n# {sheet}\n{sheet_df.to_string(index=False)}"

        if text.strip():
            texts.append(text)
            sources.append(filename)
        else:
            print(f"⚠️ Inget innehåll i: {filename}")

    return texts, sources

# ✂️ Chunka text
def chunk_text(text, size=500, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i += size - overlap
    return chunks

# 🚀 Kör pipeline
texts, files = read_documents()
chunks, sources = [], []

for text, source in zip(texts, files):
    ch = chunk_text(text)
    chunks.extend(ch)
    sources.extend([source] * len(ch))

print(f"🔢 Totalt {len(chunks)} chunkar från {len(set(files))} dokument.")

vectors = [get_embedding(c) for c in chunks]
dimension = len(vectors[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors).astype("float32"))

# 💾 Spara index
with open("data.pkl", "wb") as f:
    pickle.dump((index, chunks, sources), f)

print("✅ Klart! FAISS-index och källor sparade i data.pkl")
