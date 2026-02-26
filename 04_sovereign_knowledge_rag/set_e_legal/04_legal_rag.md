# Session 04: Sovereign Knowledge RAG (Legal)

## [INTEGRATOR] Track

### Overview
This lab ingests the **M&A Due Diligence Checklist** into ChromaDB using `nomic-embed-text` and uses a Genkit Retriever to answer M&A contract risk classification questions — grounding `llama3.2:1b` responses on verified legal standards to prevent hallucinated risk guidance.

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
Open **http://localhost:4000** → **Flows** → `legal_rag_flow` → ask M&A due diligence questions and inspect the retrieved clause context.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```

---

## [ARCHITECT] Track

### Knowledge Document
`ma_due_diligence_checklist.txt` — covers contract risk classification (LOW/MEDIUM/HIGH), uncapped liability, termination clauses, IP ownership, governing law, change of control provisions, and remediation protocol.

### Default Test Query
> *"What is the risk classification for an uncapped liability clause in an M&A contract?"*

### Validation Output
```
[STEP 1] Loading ma_due_diligence_checklist.txt...
[STEP 2] Embedding 5 chunks... → indexed to ChromaDB
[STEP 3] Retrieving M&A context... → 3 chunks retrieved
[STEP 4] Answer: Uncapped liability clauses are classified as HIGH risk and must be renegotiated
         to a cap equal to the contract value before signing (per M&A Checklist Section 2).
Answer saved to /tmp/legal_output/rag_answer.md
```

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
# Confirm: chunks indexed, answer cites HIGH risk classification for uncapped liability
