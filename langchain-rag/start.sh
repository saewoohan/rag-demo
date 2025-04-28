#!/bin/sh

echo "Loading data"
python ingest.py

echo "Starting server"
uvicorn main:app --host 0.0.0.0 --port 3000 