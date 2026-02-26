# ⚖️ Legal Track (Set E)

Welcome to the Legal Sovereign AI track. This curriculum focuses on contract clause parsing, due diligence memos, M&A auditor swarms, and RAG over legal checklists.

## 🗺️ Syllabus

### 1. Data Pipeline Automation
- **Goal**: Clean and parse raw M&A contract snippets for unapproved terminology.
- **Code**: [`logic/clause_scanner.py`](../01_data_pipeline_automation/set_e_legal/logic/clause_scanner.py)
- **Lab**: [**01 Legal Pipeline**](../01_data_pipeline_automation/set_e_legal/01_legal_pipeline.md)

### 2. Executive Narrative Engine
- **Goal**: Read flagged contract clauses and generate a Due Diligence Memo.
- **Code**: [`logic/due_diligence_gen.py`](../02_executive_narrative_engine/set_e_legal/logic/due_diligence_gen.py)
- **Lab**: [**02 Legal Narrative**](../02_executive_narrative_engine/set_e_legal/02_legal_narrative.md)

### 3. Multi-Agent Systems
- **Goal**: A 3-agent swarm (Analyst, Auditor, Reporter) resolving complex M&A liability risks.
- **Code**: [`logic/swarm.py`](../03_multi_agent_systems/set_e_legal/logic/swarm.py)
- **Lab**: [**03 Legal Swarm**](../03_multi_agent_systems/set_e_legal/03_legal_swarm.md)

### 4. Sovereign Knowledge RAG
- **Goal**: Retrieve ground truth from the `ma_due_diligence_checklist.txt` using Local Embeddings.
- **Code**: [`logic/ingest_and_query.py`](../04_sovereign_knowledge_rag/set_e_legal/logic/ingest_and_query.py)
- **Lab**: [**04 Legal RAG**](../04_sovereign_knowledge_rag/set_e_legal/04_legal_rag.md)

### 5. Sovereign Cockpit
- **Goal**: Expose the RAG and Swarm back to the M&A lawyer via LobeChat.
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
