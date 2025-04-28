import json
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'characters.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

documents = []

for character in data['characters']:
    doc = Document(
        page_content=f"{character['name']}: {character['description']} Features: {', '.join(character['features'])}. Category: {character['category']}",
        metadata={
            "name": character['name'],
            "category": character['category'],
            "features": ', '.join(character['features']),
            "origin": character.get('origin', 'Unknown'),
            "related_characters": ', '.join(character.get('related_characters', []))
        }
    )
    documents.append(doc)

doc = Document(
    page_content=data['metadata']['description'],
    metadata={
        "name": "metadata",
        "category": "metadata",
        "features": ', '.join(data['metadata']['key_features']),
        "trend_start": data['metadata']['trend_start'],
        "primary_platform": data['metadata']['primary_platform']
    }
)
documents.append(doc)

def ingest_documents():
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Initialize ChromaDB
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    
    # Add documents to ChromaDB
    vectorstore.add_documents(documents)
    print(f"Added {len(documents)} documents to ChromaDB")

if __name__ == "__main__":
    ingest_documents() 