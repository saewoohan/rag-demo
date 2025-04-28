from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Question(BaseModel):
    question: str

class Source(BaseModel):
    content: str
    metadata: dict

class Answer(BaseModel):
    answer: str
    sources: List[Source]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

ollama_base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
llm = Ollama(base_url=ollama_base_url, model="llama3.2:1b")

template = """Here is information about Italian Brainrot characters:

{context}

Based on the above information, please answer the following question:
{question}

Please use only the provided information to answer. If the information is insufficient, please say so."""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={
        "prompt": PROMPT
    },
    return_source_documents=True
)

@app.post("/rag/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        result = qa_chain({"query": question.question})
        
        sources = [
            Source(
                content=doc.page_content,
                metadata=doc.metadata
            )
            for doc in result["source_documents"]
        ]
        
        return Answer(
            answer=result["result"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000) 