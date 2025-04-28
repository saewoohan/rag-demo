from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from typing import List
import logging
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""
torch.set_num_threads(4)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("Starting to load the model...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

@app.post("/embed")
async def create_embedding(input: TextInput):
    try:
        embedding = model.encode(input.text)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed_batch")
async def create_batch_embedding(input: BatchTextInput):
    try:
        embeddings = model.encode(input.texts)
        return {"embeddings": embeddings.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
