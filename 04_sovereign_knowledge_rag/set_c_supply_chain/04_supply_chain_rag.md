# Session 04: Sovereign Knowledge RAG (Supply Chain)

## [INTEGRATOR] Track

### Overview
This lab ingests the **Warehouse Standard Operating Procedures** into a ChromaDB vector store and uses a Genkit Retriever to answer operational questions about SKU formats, stock quantity validation, and reorder protocols — all grounded on the local knowledge base.

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
Open **http://localhost:4000** → **Flows** → `supply_chain_rag_flow` → ask SOP questions and inspect retrieved context.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/ingest_and_query.py
```

---

## [ARCHITECT] Track

### Knowledge Document
`warehouse_sop.txt` — covers SKU format standards, stock quantity validation, unit price integrity, restock date requirements, supplier lead times, and audit protocols.

### Default Test Query
> *"What is the correct format for a SKU and what happens if it is malformed?"*

### Validation Output
```
[STEP 1] Loading warehouse_sop.txt...
[STEP 2] Embedding 5 chunks... → indexed to ChromaDB
[STEP 3] Retrieving SOP context... → 3 chunks retrieved
[STEP 4] Answer: SKUs must follow PREFIX-NUMBERS format (e.g., WH-9942). Malformed SKUs
         cannot be committed to shipment orders (per SOP Section 2).
Answer saved to /tmp/supply_chain_output/rag_answer.md
```

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/ingest_and_query.py
# Confirm: chunks indexed, answer cites SOP SKU format requirements

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 03](../../03_multi_agent_systems/set_c_supply_chain/03_supply_chain_swarm.md) | [Next Lab: Session 05](../../05_advanced_ui_lobechat/05_advanced_ui_lobechat.md)**
