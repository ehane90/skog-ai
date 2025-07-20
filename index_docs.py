import os
import pickle
import faiss
import numpy as np

from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📂 Läs dokument från mappen
doc_folder = "docs"
all_texts = []
sources = []

for filename in os.listdir(doc_folder):
    path = os.path.join(doc_folder, filename)
    print(f"Läser in: {path}")

    text = ""
    if filename.endswith(".pdf"):
        with open(path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

    elif filename.endswith(".docx"):
        doc = DocxDocument(path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    elif filename.endswith(".xls") or filename.endswith(".xlsx"):
        df = pd.read_excel(path, sheet_name=None)
        for sheet, sheet_df in df.items():
            text += f"\n\n# {sheet}\n"
            text += sheet_df.to_string(index=False)

    else:
        print(f"⚠️ Hoppar över okänd filtyp: {filename}")
        continue

    if len(text.strip()) == 0:
        print(f"⚠️ Inget innehåll i: {filename}")
        continue

    all_texts.append(text)
    sources.append(filename)

# 🔪 Dela upp text i chunkar
def chunk_text(text, max_length=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_length - overlap
    return chunks

chunks = []
chunk_sources = []

for text, source in zip(all_texts, sources):
    c = chunk_text(text)
    chunks.extend(c)
    chunk_sources.extend([source] * len(c))

# 🔐 Skapa embeddings
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

print(f"🔢 Skickar {len(chunks)} chunkar till OpenAI...")

vectors = np.array([get_embedding(c) for c in chunks]).astype("float32")
dimension = vectors.shape[1]

# 🧠 Skapa FAISS-index
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# 💾 Spara data
with open("data.pkl", "wb") as f:
    pickle.dump((index, chunks, chunk_sources), f)

print("✅ Klart! Embeddings sparade i data.pkl")
import os
import pickle
import numpy as np
import openai
import faiss
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
from dotenv import load_dotenv

# 🟢 Läs in API-nyckel från miljövariabler
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 Embedding-funktion
def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

# 📚 Läs alla dokument
def read_documents(folder):
    texts, files = [], []
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        print(f"Läser in: {f}")

        if f.endswith(".pdf"):
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif f.endswith(".docx"):
            doc = Document(path)
            text = "\n".join([para.text for para in doc.paragraphs])

        elif f.endswith(".xlsx") or f.endswith(".xls"):
            try:
                df = pd.read_excel(path, sheet_name=None)
                text = "\n".join([
                    df[sheet].to_string(index=False)
                    for sheet in df
                ])
            except Exception as e:
                print(f"⚠️ Kunde inte läsa {f}: {e}")
                continue

        else:
            continue  # hoppa okända filer

        texts.append(text)
        files.append(f)
    return texts, files

# 🧩 Chunka text
def chunk_text(text, size=500):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

# 🔁 Kör hela pipelinen
texts, files = read_documents("docs")
chunks, sources = [], []

for text, filename in zip(texts, files):
    for chunk in chunk_text(text):
        chunks.append(chunk)
        sources.append(filename)

print(f"🔢 Skickar {len(chunks)} chunkar till OpenAI...")

embeddings = [get_embedding(c) for c in chunks]

# 📦 Indexera i FAISS
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings).astype("float32"))

# 💾 Spara som pickle
with open("data.pkl", "wb") as f:
    pickle.dump((index, chunks, sources), f)

print("✅ Klart! Embeddings sparade i data.pkl")
import os
import faiss
import openai
import numpy as np
from PyPDF2 import PdfReader
def get_embedding(text, model="text-embedding-3-small"):
    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

import pickle
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.project = os.getenv("OPENAI_PROJECT_ID")

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
