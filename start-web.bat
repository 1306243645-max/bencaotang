@echo off
cd /d C:\Users\Admin\agent-workstation
echo Starting BenCao Tang - TCM Web Interface...
.venv\Scripts\streamlit.exe run web/app.py --server.headless true
pause
