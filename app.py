import streamlit as st
import openai
import numpy as np
import faiss
import pickle
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("data.pkl", "rb") as f:
    index, chunks, sources = pickle.load(f)

def get_embedding(text):
    return openai.Embedding.create(input=[text], model="text-embedding-3-small")["data"][0]["embedding"]

def query_rag(question, k=3):
    query_vec = np.array(get_embedding(question)).astype("float32")
    D, I = index.search(np.array([query_vec]), k)
    context = "\n\n".join([chunks[i] for i in I[0]])
    prompt = f"Besvara frågan baserat på följande text:\n\n{context}\n\nFråga: {question}"
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return result["choices"][0]["message"]["content"]

st.title("Norra Vränglarp AI")
q = st.text_input("Ställ din fråga:")

if st.button("Sök"):
    if q:
        svar = query_rag(q)
        st.markdown("### Svar:")
        st.write(svar)
