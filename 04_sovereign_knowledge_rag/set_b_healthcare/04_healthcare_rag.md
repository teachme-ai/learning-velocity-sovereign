# Session 04: Sovereign Knowledge RAG (Healthcare)

## [INTEGRATOR] Track

### Overview
This lab builds a HIPAA-aware sovereign RAG pipeline that ingests the **HIPAA Billing Compliance Guide** into ChromaDB using `nomic-embed-text` embeddings. A Genkit-native Retriever then surfaces the most relevant compliance clauses to ground `llama3.2:1b`'s answers.

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
Open **http://localhost:4000** → **Flows** → `healthcare_rag_flow` → ask HIPAA compliance questions and trace retrieved context.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```

---

## [ARCHITECT] Track

### Knowledge Document
`hipaa_billing_guide.txt` — covers ICD-10 code validation, billing amount thresholds, PII anonymization, claim submission deadlines, and common violation remediation.

### Default Test Query
> *"What should happen when a billing record contains a negative amount?"*

### Validation Output
```
[STEP 1] Loading hipaa_billing_guide.txt...
[STEP 2] Embedding and indexing... → vectors stored in ChromaDB
[STEP 3] Retrieving HIPAA context... → 3 chunks retrieved
[STEP 4] Answer: Negative billing amounts indicate a data integrity violation and must be
         quarantined for manual review before claim submission (per HIPAA Section 3).
Answer saved to /tmp/healthcare_output/rag_answer.md
```

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
# Confirm: chunks indexed, answer cites the HIPAA negative-amount policy
