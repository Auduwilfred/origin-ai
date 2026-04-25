#!/bin/bash
echo 'Starting Origin AI...'
uvicorn app.main:app --reload &
streamlit run frontend/app.py &
streamlit run frontend/admin.py --server.port 8502 &
