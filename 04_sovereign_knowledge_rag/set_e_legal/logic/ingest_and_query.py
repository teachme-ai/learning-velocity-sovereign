"""
Session 04 — Set E: Legal Sovereign RAG
Native Google Genkit Retriever pattern backed by ChromaDB + Ollama nomic-embed-text.
Run with: genkit start -- /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
"""
from pathlib import Path
import chromadb
from pydantic import BaseModel, Field
from genkit.ai import Genkit, Document
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition
from genkit.plugins.ollama.embedders import EmbeddingDefinition
from genkit.types import RetrieverRequest, RetrieverResponse, ActionRunContext

BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "ma_due_diligence_checklist.txt"
CHROMA_DIR = str(BASE_DIR / "data" / "chroma_db")
COLLECTION = "legal_policy"
QUERY = "What is the risk classification for an uncapped liability clause in an M&A contract?"

ai = Genkit(
    plugins=[
        Ollama(
            models=[ModelDefinition(name="llama3.2:1b")],
            embedders=[EmbeddingDefinition(name="nomic-embed-text")],
            server_address="http://localhost:11434",
        )
    ]
)

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(COLLECTION)

def embed_text(text: str) -> list[float]:
    import ollama as _ollama
    r = _ollama.embed(model="nomic-embed-text", input=text)
    return r["embeddings"][0]

async def ingest():
    print(f"[STEP 1] Loading {DATA_FILE.name}...")
    text = DATA_FILE.read_text()
    chunks = [text[i:i+500] for i in range(0, len(text), 450)]
    col = get_collection()
    print(f"[STEP 2] Embedding {len(chunks)} chunks...")
    for i, chunk in enumerate(chunks):
        col.upsert(ids=[f"chunk_{i}"], documents=[chunk], embeddings=[embed_text(chunk)])
    print(f"         → Indexed to {CHROMA_DIR}")

async def legal_retriever(request: RetrieverRequest, ctx: ActionRunContext) -> RetrieverResponse:
    embedding = embed_text(request.query.text())
    results = get_collection().query(query_embeddings=[embedding], n_results=3)
    return RetrieverResponse(documents=[Document.from_text(d) for d in results["documents"][0]])

ai.define_retriever(name="legal_policy", fn=legal_retriever)

class RAGInput(BaseModel):
    query: str = Field(description="M&A due diligence legal question")

class RAGOutput(BaseModel):
    answer: str = Field(description="Grounded M&A policy answer")

@ai.flow()
async def legal_rag_flow(input_data: RAGInput) -> RAGOutput:
    print(f"\n[STEP 3] Retrieving M&A context for: '{input_data.query}'")
    retriever_result = await ai.retrieve(query=Document.from_text(input_data.query), retriever="legal_policy")
    docs = retriever_result.documents
    response = await ai.generate(
        system="You are an M&A Legal Counsel. Answer strictly from the provided due diligence context.",
        prompt=input_data.query,
        docs=docs,
        model="ollama/llama3.2:1b",
    )
    print("\n[STEP 4] Answer:")
    print(response.text.strip())
    return RAGOutput(answer=response.text.strip())

async def main():
    print("\n--- Legal Sovereign RAG Pipeline ---")
    await ingest()
    result = await legal_rag_flow(RAGInput(query=QUERY))
    out = Path("/tmp/legal_output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "rag_answer.md").write_text(f"# Query\n{QUERY}\n\n# Answer\n{result.answer}")
    print(f"\nAnswer saved to /tmp/legal_output/rag_answer.md")

if __name__ == "__main__":
    ai.run_main(main())

