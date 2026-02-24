import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI App
app = FastAPI(
    title="Sovereign Audit Standards API",
    description="Query corporate policies using a local FAISS RAG pipeline.",
    version="1.0.0"
)

# Allow CORS for LobeChat to call this API directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Models (Lazy Loaded to prevent immediate DB crashes on startup)
embeddings = None
rag_chain = None

def get_rag_chain():
    global embeddings, rag_chain
    if rag_chain is not None:
        return rag_chain

    base_dir = Path(__file__).parent.parent
    db_path = base_dir / "db"

    if not db_path.exists():
        raise RuntimeError("Vector database not found. Please run ingest_and_query.py first.")

    print("Loading Local FAISS Database...")
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest",
        base_url="http://localhost:11434"
    )
    vectorstore = FAISS.load_local(
        str(db_path), 
        embeddings, 
        allow_dangerous_deserialization=True # Required for local trusted FAISS
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = OllamaLLM(
        model="llama3.2:1b",
        base_url="http://localhost:11434",
        temperature=0
    )

    prompt = PromptTemplate.from_template(
        "You are an expert HR and Audit assistant. Answer the question based ONLY on the following context:\n\n"
        "Context: {context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# API Schemas
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    # Pre-load the DB on API startup
    try:
        get_rag_chain()
        print("Sovereign RAG API Successfully Initialized.")
    except Exception as e:
        print(f"Warning on startup: {e}")

@app.post("/query", response_model=QueryResponse, summary="Query the Policy Database")
async def query_policy(request: QueryRequest):
    """
    Submit a query against the automated corporate travel and expense policies.
    """
    try:
        chain = get_rag_chain()
        response = chain.invoke(request.query)
        return QueryResponse(answer=response.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # If run directly, start the server on Port 8000
    uvicorn.run("04_sovereign_knowledge_rag.logic.api:app", host="0.0.0.0", port=8000, reload=True)
