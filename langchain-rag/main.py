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

# Initialize components
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize ChromaDB
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Initialize Ollama
ollama_base_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
llm = Ollama(base_url=ollama_base_url, model="mistral")

# Create prompt template
template = """다음은 Italian Brainrot 캐릭터들에 대한 정보입니다:

{context}

위 정보를 바탕으로 다음 질문에 답변해주세요:
{question}

가능한 한 주어진 정보만을 사용하여 답변해주세요. 정보가 불충분하다면 그렇다고 말씀해주세요."""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# Initialize RAG chain
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
        # Get answer from RAG chain
        result = qa_chain({"query": question.question})
        
        # Format sources
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