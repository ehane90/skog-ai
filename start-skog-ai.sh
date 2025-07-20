#!/bin/bash

# Aktivera miljövariabler
source ~/.bashrc
source ~/skog-ai/venv/bin/activate

# Döda gamla sessioner om de finns
tmux kill-session -t streamlit 2>/dev/null
tmux kill-session -t ngrok 2>/dev/null

# Starta Streamlit i tmux-session
tmux new-session -d -s streamlit "cd ~/skog-ai && source venv/bin/activate && streamlit run app.py --server.address=0.0.0.0 --server.port=8501"

# Vänta lite innan vi startar ngrok (så att port 8501 säkert är redo)
sleep 5

# Starta ngrok med fast domän
tmux new-session -d -s ngrok "/usr/local/bin/ngrok http --domain=skogai.ngrok.dev 8501"
