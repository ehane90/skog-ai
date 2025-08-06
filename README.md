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


##📄 Lägga till nya dokument
För att lägga till nya dokument till AI-appen (t.ex. 
skogsbruksplaner, bokslut eller andra interna filer):

1. Kör det medföljande uppladdningsskriptet
Använd upload_docs.py för att ladda upp alla dokument i en lokal 
mapp till servern:

bash
./upload_docs.py /sökväg/till/dokument
Detta skript:

Läser in alla .pdf, .docx, .xls, .xlsx-filer från den angivna 
mappen

Hoppar över filer som redan finns i docs/ (baserat på filnamn)

Kopierar de nya filerna till servern via scp

Du kan konfigurera upload_docs.py så att din server-IP, sökvägar 
och SSH-nyckel är förifyllda – praktiskt om du laddar upp ofta.

2. Indexera dokumenten på servern
Logga in på servern (via SSH eller tmux) och kör:

bash
cd skog-ai
source venv/bin/activate
python index_docs.py

Detta uppdaterar data.pkl med de nya dokumentens chunkar och 
embeddings.

3. Starta om appen
Om appen körs i bakgrunden (t.ex. via tmux), starta om den för att 
ladda in nya dokument:

bash
./start-skog-ai.sh

