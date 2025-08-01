#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--- Installing Python dependencies ---"
pip install --no-cache-dir -r requirements.txt

echo "--- Installing Node.js dependencies ---"
cd frontend
npm ci --only=production

echo "--- Cleaning old frontend build ---"
rm -rf dist

echo "--- Building React frontend ---"
npm run build
cd ..

echo "--- Starting FastAPI server ---"
gunicorn -w 2 -k uvicorn.workers.UvicornWorker --timeout 120 --keep-alive 2 app:app 