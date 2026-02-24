import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from google.genai import types

# ── Configuration ────────────────────────────────────────────────────────────

SESSION_DIR = Path(__file__).resolve().parent.parent
DB_PATH     = SESSION_DIR / "data" / "chroma_db"
POLICY_PATH = SESSION_DIR / "data" / "corporate_policy_2026.md"

# Fully local embedding model
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
GEN_MODEL        = "gemini-2.0-flash"
COLLECTION_NAME  = "sovereign_vault_local"

# ── Initialization ────────────────────────────────────────────────────────────

# Initialize local embedding function (Sentence Transformers)
# This downloads the model on the first run and runs locally thereafter.
local_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL_NAME)

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=str(DB_PATH))
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ── Core Functions ────────────────────────────────────────────────────────────

def ingest_policy():
    """Chunk and index the corporate policy markdown using local embeddings."""
    print(f"\n[1/3] Reading policy: {POLICY_PATH.name}")
    
    if not POLICY_PATH.exists():
        print(f"[ERROR] Policy file missing at {POLICY_PATH}")
        return

    content = POLICY_PATH.read_text(encoding="utf-8")
    
    # Chunking logic (by markdown header)
    print(f"[2/3] Chunking text into semantically distinct units...")
    chunks = [c.strip() for c in content.split("##") if c.strip()]
    
    print(f"[3/3] Indexing in ChromaDB (Model: {EMBED_MODEL_NAME})...")
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=local_ef
    )

    for i, chunk in enumerate(chunks):
        collection.upsert(
            ids=[f"rule_{i}"],
            documents=[chunk],
            metadatas=[{"source": POLICY_PATH.name}]
        )
    print(f"✅ Vault updated with {len(chunks)} local embeddings.")

def ask_the_vault(question: str):
    """The 'Evidence-First' Loop: Retrieval + Grounded Verification."""
    print(f"\n" + "═"*60)
    print(f"QUESTION: {question}")
    print("═"*60)
    
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=local_ef)
    
    # 1. Semantic Retrieval
    results = collection.query(
        query_texts=[question],
        n_results=1
    )
    
    if not results['documents'] or not results['documents'][0]:
        print("[ERROR] No policy evidence found.")
        return

    evidence = results['documents'][0][0]
    
    # Display the Evidence first (as requested)
    print(f"📜 [EVIDENCE]:\n{evidence}\n")

    # 2. Grounded Generation via Gemini 2.0
    prompt = (
        f"Using ONLY the following policy snippet as evidence, answer the question. "
        f"If the answer is NOT explicitly supported by the snippet, you must say: "
        f"'I do not have the authority to answer based on current policy.'\n\n"
        f"EVIDENCE:\n{evidence}\n\n"
        f"QUESTION: {question}"
    )

    try:
        response = gemini_client.models.generate_content(
            model=GEN_MODEL,
            contents=prompt
        )
        print(f"🤖 [SOVEREIGN RESPONSE]:\n{response.text}")
    except Exception as e:
        print(f"[ERROR] Gemini Generation failed: {e}")

# ── Interactive / Test Execution ──────────────────────────────────────────────

if __name__ == "__main__":
    # Ensure fresh ingestion
    ingest_policy()
    
    # Scenario A: In-Policy Query
    ask_the_vault("Can I expense a $500 ergonomic chair?")
    
    # Scenario B: Out-of-Policy Query
    ask_the_vault("What is the reimbursement policy for pet insurance?")
