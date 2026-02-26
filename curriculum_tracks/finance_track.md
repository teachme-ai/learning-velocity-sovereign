# 🏦 Finance Track (Set A)

Welcome to the Finance Sovereign AI track. This curriculum focuses on financial data scrubbing, expense anomaly detection, Executive Audit Board memos, and RAG over corporate policies.

## 🗺️ Syllabus

### 1. Data Pipeline Automation
- **Goal**: Scrub and classify raw transaction logs into flagged expenses.
- **Code**: [`logic/cleaner.py`](../01_data_pipeline_automation/set_a_finance/logic/cleaner.py)
- **Lab**: [**01 Finance Pipeline**](../01_data_pipeline_automation/01_data_pipeline_automation.md)

### 2. Executive Narrative Engine
- **Goal**: Read flagged transactions and generate a Board-level Audit Memo using LLM prompting.
- **Code**: [`logic/narrative_gen.py`](../02_executive_narrative_engine/set_a_finance/logic/narrative_gen.py)
- **Lab**: [**02 Finance Narrative**](../02_executive_narrative_engine/02_executive_narrative_engine.md)

### 3. Multi-Agent Systems
- **Goal**: A 3-agent swarm (Analyst, Auditor, Reporter) resolving complex anomalies.
- **Code**: [`logic/swarm.py`](../03_multi_agent_systems/set_a_finance/logic/swarm.py)
- **Lab**: [**03 Finance Swarm**](../03_multi_agent_systems/set_a_finance/03_finance_swarm.md)

### 4. Sovereign Knowledge RAG
- **Goal**: Retrieve ground truth from `corporate_policy.txt` using Local Embeddings.
- **Code**: [`logic/ingest_and_query.py`](../04_sovereign_knowledge_rag/set_a_finance/logic/ingest_and_query.py)
- **Lab**: [**04 Finance RAG**](../04_sovereign_knowledge_rag/set_a_finance/04_finance_rag.md)

### 5. Sovereign Cockpit
- **Goal**: Expose the RAG and Swarm back to the end-user via LobeChat.
- **Lab**: [**05 LobeChat UI**](../05_advanced_ui_lobechat/05_advanced_ui_lobechat.md)

### 6. Sovereign Observability
- **Goal**: Trace Agent steps to ensure exact compliance and auditability.
- **Lab**: [**06 Observability**](../06_observability/06_sovereign_tracing.md)

### 7. Enterprise Auth (Architecting)
- *Coming Soon*

### 8. Capstone Production (Architecting)
- *Coming Soon*

---
**[Back to Curriculum Hub](../README.md)**
