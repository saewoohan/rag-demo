FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Remove any existing ChromaDB data and then run ingest
RUN rm -rf chroma_db && python ingest.py

CMD ["python", "main.py"] 