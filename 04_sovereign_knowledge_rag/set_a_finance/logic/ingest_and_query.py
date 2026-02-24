import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Use Nomic Embeddings from local Ollama
embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
    base_url="http://localhost:11434"
)

# Use Qwen or Llama 3.2 for the generation step
llm = OllamaLLM(
    model="llama3.2:1b",
    base_url="http://localhost:11434",
    temperature=0
)

def build_and_query_rag():
    print("\n--- Sovereign Knowledge: RAG Pipeline ---")
    
    # Paths
    base_dir = Path(__file__).parent.parent
    data_path = base_dir / "data" / "travel_policy.txt"
    db_path = base_dir / "db"
    
    # 1. Loading Text
    print("[STEP 1] Loading document...")
    loader = TextLoader(str(data_path))
    docs = loader.load()
    print(f" [OK] Loaded {len(docs)} document(s).")
    
    # 2. Splitting Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f" [OK] Split into {len(splits)} chunks.")
    
    # 3. Embedding and Vector Store
    print("[STEP 2] Generating Local Embeddings & Storing with FAISS...")
    if db_path.exists():
        import shutil
        shutil.rmtree(db_path)
    
    db_path.mkdir(parents=True, exist_ok=True)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    vectorstore.save_local(str(db_path))
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    print(" [OK] Vector store initialized at /db.")
    
    # 4. RAG Query Execution
    query = "What is the limit for daily meal expenses?"
    print(f"\n[STEP 3] Executing Query: '{query}'")
    
    prompt = PromptTemplate.from_template(
        "You are an expert HR assistant. Answer the question based ONLY on the following context:\n\n"
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
    
    # Generate Response
    response = rag_chain.invoke(query)
    
    print("\n--- AI Response ---")
    print(response.strip())
    print("\n--- Pipeline Complete ---")

if __name__ == "__main__":
    build_and_query_rag()
