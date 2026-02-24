"""
vault_builder.py — The Architect's Build
Session 04: Sovereign Knowledge RAG — Local Private Intelligence

This script implements a local RAG pipeline:
1. Ingests corporate_policy.pdf (local asset)
2. Chunks text using recursive character splitting
3. Embeds chunks using Ollama (nomic-embed-text)
4. Stores in a persistent local ChromaDB collection
5. Performs semantic retrieval for user queries

Prerequisites:
- Ollama installed and running
- Model pulled: ollama pull nomic-embed-text
"""

import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
import ollama
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── Configuration ────────────────────────────────────────────────────────────

SESSION_DIR = Path(__file__).resolve().parent.parent
DB_PATH     = SESSION_DIR / "data" / "chroma_db"
PDF_PATH    = SESSION_DIR / "assets" / "data" / "corporate_policy.pdf"

EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "corporate_rules"

# ── Initialization ────────────────────────────────────────────────────────────

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=str(DB_PATH))

def get_embedding(text: str):
    """Fetch embedding from local Ollama instance."""
    try:
        response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"[ERROR] Ollama failed: {e}")
        print(f"Ensure Ollama is running and you have run: ollama pull {EMBED_MODEL}")
        return None

# ── Core Functions ────────────────────────────────────────────────────────────

def ingest_policy():
    """Load, chunk, and index the corporate policy PDF."""
    print(f"\n[1/3] Reading policy from {PDF_PATH.name}...")
    
    if not PDF_PATH.exists():
        print(f"[ERROR] PDF not found at {PDF_PATH}")
        return

    # Extract text from PDF
    text = ""
    try:
        reader = PdfReader(PDF_PATH)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"[WARNING] PDF reader failed (file might be plain text): {e}")
        text = PDF_PATH.read_text(encoding="utf-8")

    if not text.strip():
        print("[ERROR] No text extracted from policy.")
        return

    print(f"[2/3] Chunking text (RecursiveCharacterTextSplitter)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    print(f"      Split into {len(chunks)} chunks.")

    print(f"[3/3] Indexing in ChromaDB...")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Prepare IDs and Embeddings
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = []
    
    for i, chunk in enumerate(chunks):
        embed = get_embedding(chunk)
        if embed:
            embeddings.append(embed)
        else:
            print(f"      [SKIP] Failed to embed chunk {i}")

    # Add to collection
    if embeddings:
        collection.add(
            ids=ids[:len(embeddings)],
            embeddings=embeddings,
            documents=chunks[:len(embeddings)]
        )
        print(f"✅ Vault updated with {len(embeddings)} entries.")

def query_vault(question: str):
    """Retrieve relevant clauses and answer the question."""
    print(f"\n--- QUERYING VAULT: {question} ---")
    
    collection = client.get_collection(name=COLLECTION_NAME)
    
    # Embed the question
    query_embed = get_embedding(question)
    if not query_embed:
        return

    # Retrieval
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=2
    )

    print("\n[RETRIEVED CONTEXT]")
    for i, doc in enumerate(results['documents'][0]):
        print(f"Clause {i+1}: {doc.strip()[:200]}...")

    print("\n[SOVEREIGN ANSWER]")
    context = "\n".join(results['documents'][0])
    
    # We use Ollama again for the final generation
    prompt = (
        f"You are a Sovereign Policy Assistant. Answer the question based ONLY "
        f"on the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
    )
    
    try:
        response = ollama.generate(model="llama3.2:1b", prompt=prompt)
        print(response['response'])
    except Exception as e:
        print(f"[ERROR] Answer generation failed: {e}")

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Ensure corporate_policy.pdf exists (creating it if missing for student convenience)
    if not PDF_PATH.exists():
        print("[INFO] Creating stub corporate_policy.pdf...")
        PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
        # For simplicity in this lab, we'll treat the copy we made as the file
        # In a real lab, students would provide a proper PDF.
    
    # Step 1: Ingest
    ingest_policy()
    
    # Step 2: Test Query
    query_vault("What is the maximum limit for technology expenses?")
    query_vault("Who needs to approve expenses over $10,000?")
