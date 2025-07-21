#!/usr/bin/env bash
# Exit on error
set -o errexit

# --- Install Dependencies ---
echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Installing Node.js dependencies ---"
cd frontend
npm install
cd ..

# --- Build Frontend ---
echo "--- Building React frontend ---"
cd frontend
npm run build
cd ..

# --- Run Application ---
echo "--- Starting FastAPI server ---"
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app 