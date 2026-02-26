# Session 04: Sovereign Knowledge RAG (EdTech)

## [INTEGRATOR] Track

### Overview
This lab ingests the **Academic Integrity and Learning Management Policy** into ChromaDB using `nomic-embed-text` and uses a Genkit Retriever to answer questions about LMS data validation, score range rules, and academic misconduct procedures — grounded on actual policy text.

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
Open **http://localhost:4000** → **Flows** → `edtech_rag_flow` → ask academic integrity policy questions and inspect retrieved context.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```

---

## [ARCHITECT] Track

### Knowledge Document
`academic_integrity_policy.txt` — covers valid score ranges (0–100), time spent validation, learning decay definition, academic dishonesty protocol, and LMS vendor obligations.

### Default Test Query
> *"What is the procedure when a student score exceeds 100 in the LMS?"*

### Validation Output
```
[STEP 1] Loading academic_integrity_policy.txt...
[STEP 2] Embedding 5 chunks... → indexed to ChromaDB
[STEP 3] Retrieving policy context... → 3 chunks retrieved
[STEP 4] Answer: A score exceeding 100 indicates either an LMS configuration error or
         deliberate grade manipulation and must be investigated (per Policy Section 2).
Answer saved to /tmp/edtech_output/rag_answer.md
```

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
# Confirm: chunks indexed, answer cites LMS score range policy

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 03](../../03_multi_agent_systems/set_d_edtech/03_edtech_swarm.md) | [Next Lab: Session 05](../../05_advanced_ui_lobechat/05_advanced_ui_lobechat.md)**
