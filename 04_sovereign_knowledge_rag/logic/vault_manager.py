import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
import ollama
from google import genai
from google.genai import types

# ── Configuration ────────────────────────────────────────────────────────────

SESSION_DIR = Path(__file__).resolve().parent.parent
DB_PATH     = SESSION_DIR / "data" / "chroma_db"
POLICY_PATH = SESSION_DIR / "data" / "corporate_policy_2026.md"

EMBED_MODEL = "nomic-embed-text"
GEN_MODEL   = "gemini-2.0-flash"
COLLECTION_NAME = "sovereign_vault"

# ── Initialization ────────────────────────────────────────────────────────────

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=str(DB_PATH))
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_embedding(text: str):
    """Fetch embedding from local Ollama instance."""
    try:
        response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
        return response["embedding"]
    except Exception as e:
        print(f"[ERROR] Ollama failed: {e}")
        return None

# ── Core Functions ────────────────────────────────────────────────────────────

def ingest_policy():
    """Chunk and index the corporate policy markdown."""
    print(f"\n[1/3] Reading policy from {POLICY_PATH.name}...")
    
    if not POLICY_PATH.exists():
        print(f"[ERROR] Policy file not found at {POLICY_PATH}")
        return

    content = POLICY_PATH.read_text(encoding="utf-8")
    
    # Simple chunking by section for this exercise
    print(f"[2/3] Chunking text...")
    chunks = [c.strip() for c in content.split("##") if c.strip()]
    print(f"      Split into {len(chunks)} sections.")

    print(f"[3/3] Indexing in ChromaDB...")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    for i, chunk in enumerate(chunks):
        embed = get_embedding(chunk)
        if embed:
            collection.upsert(
                ids=[f"rule_{i}"],
                embeddings=[embed],
                documents=[chunk]
            )
    print(f"✅ Vault updated with {len(chunks)} entries.")

def ask_the_vault(question: str):
    """Grounded Query: Retrieval + Verification."""
    print(f"\n--- QUERY: {question} ---")
    
    collection = client.get_collection(name=COLLECTION_NAME)
    
    # 1. Embed the question
    query_embed = get_embedding(question)
    if not query_embed: return

    # 2. Semantic Search
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=1
    )
    
    snippet = results['documents'][0][0] if results['documents'] else "No relevant policy found."
    print(f"[VAULT CONTEXT]: {snippet[:150]}...")

    # 3. Grounded Generation via Gemini
    prompt = (
        f"Using ONLY the provided policy snippet, answer this question: {question}. "
        f"If the answer isn't in the snippet, say 'I do not have the authority to answer based on current policy.'\n\n"
        f"POLICY SNIPPET:\n{snippet}"
    )

    try:
        response = gemini_client.models.generate_content(
            model=GEN_MODEL,
            contents=prompt
        )
        print(f"\n[SOVEREIGN RESPONSE]:\n{response.text}")
    except Exception as e:
        print(f"[ERROR] Gemini Generation failed: {e}")

# ── Execution ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Ingest if DB is empty or force update
    ingest_policy()
    
    # Test 1: Valid Query
    ask_the_vault("What is the lodging limit for domestic travel?")
    
    # Test 2: Out of Policy Query
    ask_the_vault("Can I get a subscription for Netflix?")
