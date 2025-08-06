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



##  Lägga till nya dokument
För att lägga till fler dokument till appen (t.ex. 
skogsbruksplaner, bokslut eller andra filer som ska indexeras):

1. Kopiera dokument till docs/-mappen
Appen stödjer följande format:

PDF (.pdf)

Word (.docx)

Excel (.xls, .xlsx)

Du kan manuellt kopiera in filerna till docs/-mappen, eller 
använda det medföljande scriptet:

bash
Kopiera
Redigera
python upload_docs.py /sökväg/till/dokument
Scriptet:

laddar upp alla filer från en vald mapp

hoppar över filer som redan finns i docs/ (baserat på filnamn)

2. Kör om indexeringen
Efter att du lagt till nya dokument, kör om index_docs.py för att 
uppdatera embeddings:

bash
Kopiera
Redigera
source venv/bin/activate
python index_docs.py
Detta genererar en uppdaterad data.pkl med alla chunkade och 
indexerade dokument.

3. Starta om appen (om nödvändigt)
Om du kör appen via tmux, eller med startscriptet, starta om för 
att ladda in det nya data.pkl:

bash
Kopiera
Redigera
./start-skog-ai.sh
Appen är nu uppdaterad med de nya dokumenten.


