#!/usr/bin/env bash
# Exit on error
set -o errexit

# --- Install Dependencies ---
echo "--- Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- Installing Node.js dependencies ---"
cd frontend
npm install

echo "--- Cleaning old frontend build ---"
rm -rf dist

# --- Build Frontend ---
echo "--- Building React frontend ---"
npm run build
cd ..

# --- Run Application ---
echo "--- Starting FastAPI server ---"
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app 