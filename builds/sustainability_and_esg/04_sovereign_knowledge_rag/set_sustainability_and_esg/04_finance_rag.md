Here are the revised sections:

## [INTEGRATOR] Track

### Overview
This lab builds a **fully local, sovereign RAG pipeline** using **Google Genkit** (Python), **ChromaDB** (vector store), and **Ollama** (embeddings + generation). The system ingests the Corporate Travel & Expense Policy, embeds it using `nomic-embed-text`, indexes it into ChromaDB, then uses a **Genkit-native Retriever** to retrieve relevant context and generate a grounded, cited answer using `llama3.2:1b`.

### Environment Setup
```bash
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic chromadb
ollama pull llama3.2:1b && ollama pull nomic-embed-text
```

### Running the Genkit Developer UI
```bash
npm install -g genkit-cli
genkit start -- /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```
Open **http://localhost:4000** → **Flows** → `sustainability_and_esg_rag_flow` → run with any policy question and inspect the retrieved context chunks in the trace viewer.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```

---

## [ARCHITECT] Track

### RAG Architecture
```
travel_policy.txt
      │ chunk (500 chars)
      ▼
nomic-embed-text (Ollama) → vector embeddings
      │
      ▼
ChromaDB (PersistentClient)
      │
      ▼
ai.define_retriever("sustainability_and_esg_policy") → ai.retrieve()
      │ top-3 semantic chunks
      ▼
ai.generate(system + docs + query) → llama3.2:1b
      │
      ▼
Grounded Answer → /tmp/sustainability_and_esg_output/rag_answer.md
```

### Genkit Retriever Pattern
```python
async def sustainability_and_esg_retriever(request: RetrieverRequest, ctx: ActionRunContext):
    embedding = embed_text(request.query.text())
    results = chroma_collection.query(query_embeddings=[embedding], n_results=3)
    return RetrieverResponse(documents=[Document.from_text(d) for d in results["documents"][0]])

ai.define_retriever(name="sustainability_and_esg_policy", fn=sustainability_and_esg_retriever)

@ai.flow()
async def sustainability_and_esg_rag_flow(input_data: RAGInput) -> RAGOutput:
    retriever_result = await ai.retrieve(
        query=Document.from_text(input_data.query),
        retriever="sustainability_and_esg_policy"
    )
    response = await ai.generate(docs=retriever_result.documents, ...)
```

### Validation Output
```
[STEP 1] Loading and chunking travel_policy.txt... → 3 chunks
[STEP 2] Embedding and indexing with ChromaDB... → 3 vectors stored
[STEP 3] Retrieving relevant policy context...   → 3 chunks retrieved
[STEP 4] Answer: The maximum daily meal expense for domestic travel is $50.
Answer saved to /tmp/sustainability_and_esg_output/rag_answer.md
```

---

# [VALIDATE]
# Confirm the groundings (context chunks) are related to the input query and sufficient context
[STEP 1] Check that the retrieved chunks match the expected result
Confirm that the 3 top-ranking semantic chunks were generated correctly

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 03](../../03_multi_agent_systems/set_a_sustainability_and_esg/03_ # Limit context window