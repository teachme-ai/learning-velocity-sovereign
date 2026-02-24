# Lab Notes: Session 04 — Sovereign Knowledge RAG
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 Objective
Initialize a local vector database, ingest the 2026 Corporate Policy, and perform a "Grounded" retrieval query to check an ergonomic stipend claim.

---

## 🛠️ Step 1: Environment Initialization
Students must ensure the RAG stack is installed and the local embedding model is ready.

```bash
# 1. Install RAG Dependencies
pip install chromadb sentence-transformers google-generativeai pypdf

# 2. Set API Key (for Grounded Generation)
export GEMINI_API_KEY="your_api_key_here"
```

---

## 🔒 Step 2: Running the Vault Manager
Execute the logic to benchmark the "Evidence-First" loop.

```bash
# 3. Ingest and Query
python3 logic/vault_manager.py
```

---

## 📜 Capture: Execution Evidence

### [INTEGRATOR / ARCHITECT] Verified Output
```text
[1/3] Reading policy: corporate_policy_2026.md
[2/3] Chunking text into semantically distinct units...
[3/3] Indexing in ChromaDB (Model: all-MiniLM-L6-v2)...
✅ Vault updated with 4 local embeddings.

════════════════════════════════════════════════════════════
QUESTION: Can I expense a $500 ergonomic chair?
════════════════════════════════════════════════════════════
📜 [EVIDENCE]:
## 3. Workplace & Ergonomics
- Rule 3.1: Home office ergonomic equipment (chairs/desk) is limited to a one-time $1,000 stipend per employee.

🤖 [SOVEREIGN RESPONSE]:
Yes, you can expense a $500 ergonomic chair. According to Rule 3.1 in the policy, home office ergonomic equipment is covered by a one-time stipend of up to $1,000 per employee. Since $500 is within this limit, it is eligible for reimbursement.
```

---

## ⚖️ Test: Out-of-Policy Guardrail
```text
════════════════════════════════════════════════════════════
QUESTION: What is the reimbursement policy for pet insurance?
════════════════════════════════════════════════════════════
📜 [EVIDENCE]:
[No relevant sections found in Corporate Policy MD]

🤖 [SOVEREIGN RESPONSE]:
I do not have the authority to answer based on current policy.
```
