import os
import pickle
import numpy as np
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ✅ Ladda miljövariabler
load_dotenv()


# ✅ Streamlit-konfiguration först!
st.set_page_config(page_title="Skog-AI", page_icon="🌲")

# Initiera OpenAI-klient
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ladda FAISS-index och metadata
# Ladda index och data
with open("data.pkl", "rb") as f:
    index, chunks, sources = pickle.load(f)

# Visa hur många chunks som laddats
st.sidebar.markdown(f"📄 Antal dokumentdelar (chunks): **{len(chunks)}**")

# Visa antal unika källfiler
st.sidebar.markdown(f"📁 Unika källfiler: **{len(set(sources))}**")

# Lista upp till 10 källfiler
st.sidebar.markdown("📂 Exempel på källfiler:")
for s in list(set(sources))[:10]:
    st.sidebar.markdown(f"- `{s}`")

# Funktion för att skapa embedding av fråga
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return response.data[0].embedding

# Funktion för att söka i dokument och generera svar
def query_rag(question):
    query_vec = np.array(get_embedding(question)).astype("float32")
    D, I = index.search(np.array([query_vec]), k=3)

    top_chunks = [chunks[i] for i in I[0]]
    top_sources = [sources[i] for i in I[0]]

    messages = [
        {"role": "system", "content": "Du är en kunnig assistent specialiserad på skogsbruk och ekonomi. Svara på svenska."},
        {"role": "user", "content": f"Använd följande underlag:\n\n{top_chunks[0]}\n\n{top_chunks[1]}\n\n{top_chunks[2]}\n\nFråga: {question}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    svar = response.choices[0].message.content.strip()
    return svar, top_sources

# 🌲 Streamlit UI
st.title("🌲 Skog-AI – Norra Vränglarp")
st.write(f"Ställ en fråga baserat på {len(chunks)} dokumentutdrag från din skogsverksamhet.")

question = st.text_input("📝 Din fråga:", key="skog_ai_question_input")

if question:
    with st.spinner("🔍 Letar svar i dina dokument..."):
        try:
            answer, docs = query_rag(question)

            st.markdown("### 💬 Svar:")
            st.write(answer)

            st.markdown("### 📂 Källor:")
            for doc in docs:
                st.markdown(f"- `{doc}`")
        except Exception as e:
            st.error(f"Något gick fel: {e}")
