"""
Session 04 — Set A: Finance Sovereign RAG
Native Google Genkit Retriever pattern backed by ChromaDB + Ollama nomic-embed-text.
Run with: genkit start -- /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
"""
import os
import asyncio
from pathlib import Path
import chromadb
from pydantic import BaseModel, Field
from genkit.ai import Genkit, Document
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition
from genkit.plugins.ollama.embedders import EmbeddingDefinition
from genkit.types import RetrieverRequest, RetrieverResponse, ActionRunContext

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "travel_policy.txt"
CHROMA_DIR = str(BASE_DIR / "data" / "chroma_db")
COLLECTION = "finance_policy"
QUERY = "What is the maximum daily meal expense allowed for domestic travel?"

# ── Genkit + Ollama init ──────────────────────────────────────────────────────
ai = Genkit(
    plugins=[
        Ollama(
            models=[ModelDefinition(name="llama3.2:1b")],
            embedders=[EmbeddingDefinition(name="nomic-embed-text")],
            server_address="http://localhost:11434",
        )
    ]
)

# ── ChromaDB helpers ──────────────────────────────────────────────────────────
def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(COLLECTION)

def embed_text(text: str) -> list[float]:
    import ollama as _ollama
    r = _ollama.embed(model="nomic-embed-text", input=text)
    return r["embeddings"][0]

# ── Indexing ──────────────────────────────────────────────────────────────────
async def ingest():
    print(f"[STEP 1] Loading and chunking {DATA_FILE.name}...")
    text = DATA_FILE.read_text()
    chunks = [text[i:i+500] for i in range(0, len(text), 450)]
    print(f"         → {len(chunks)} chunks")

    col = get_collection()
    print("[STEP 2] Embedding and indexing with ChromaDB...")
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        col.upsert(ids=[f"chunk_{i}"], documents=[chunk], embeddings=[embedding])
    print(f"         → {len(chunks)} vectors stored in {CHROMA_DIR}")

# ── Genkit Retriever registration ─────────────────────────────────────────────
async def finance_retriever(request: RetrieverRequest, ctx: ActionRunContext) -> RetrieverResponse:
    query_text = request.query.text()
    query_embedding = embed_text(query_text)
    col = get_collection()
    results = col.query(query_embeddings=[query_embedding], n_results=3)
    docs = [Document.from_text(d) for d in results["documents"][0]]
    return RetrieverResponse(documents=docs)

ai.define_retriever(name="finance_policy", fn=finance_retriever)

# ── RAG Flow ──────────────────────────────────────────────────────────────────
class RAGInput(BaseModel):
    query: str = Field(description="Question to answer from the policy document")

class RAGOutput(BaseModel):
    answer: str = Field(description="Grounded answer from the policy knowledge base")

@ai.flow()
async def finance_rag_flow(input_data: RAGInput) -> RAGOutput:
    print(f"\n[STEP 3] Retrieving relevant policy context for: '{input_data.query}'")
    retriever_result = await ai.retrieve(
        query=Document.from_text(input_data.query),
        retriever="finance_policy",
    )
    docs = retriever_result.documents
    print(f"         → Retrieved {len(docs)} context chunks")

    response = await ai.generate(
        system="You are a Corporate Finance Policy expert. Answer the question strictly based on the provided context. Do not speculate.",
        prompt=input_data.query,
        docs=docs,
        model="ollama/llama3.2:1b",
    )

    print("\n[STEP 4] Answer:")
    print(response.text.strip())
    return RAGOutput(answer=response.text.strip())

# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    print("\n--- Finance Sovereign RAG Pipeline ---")
    await ingest()
    result = await finance_rag_flow(RAGInput(query=QUERY))
    out_dir = Path("/tmp/finance_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "rag_answer.md").write_text(f"# Query\n{QUERY}\n\n# Answer\n{result.answer}")
    print(f"\nAnswer saved to /tmp/finance_output/rag_answer.md")

if __name__ == "__main__":
    ai.run_main(main())

