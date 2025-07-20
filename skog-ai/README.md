# Norra Vränglarp AI

Ett AI-frågesystem för att hämta kunskap ur skogsgårdens interna dokument.  
Bygger på Retrieval-Augmented Generation (RAG).

## 📦 Installation

```bash
git clone https://github.com/ehane90/skog-ai.git
cd skog-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔐 API-nyckel

Skapa en `.env`-fil:

```env
OPENAI_API_KEY=din-nyckel-här
```

## 📁 Dokument

Lägg alla PDF:er i mappen `docs/`.

## 🧠 Skapa index

```bash
python index_docs.py
```

## 🚀 Starta app

```bash
streamlit run app.py --server.port 8501 --server.enableCORS false
```
