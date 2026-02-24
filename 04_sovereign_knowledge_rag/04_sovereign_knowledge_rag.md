# Lab 04: Sovereign Knowledge RAG — The Local Vault
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Welcome to the final session! In this lab, we build a **Sovereign Knowledge RAG** (Retrieval-Augmented Generation) pipeline. You will learn to ingest sensitive corporate documents into a local vector store and query them using a local LLM, ensuring 100% data privacy.

---

## ⚙️ 1. Environment Setup
Copy and paste this block to prepare your local RAG stack.

```bash
# 1. Create and Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install RAG Architecture Components
pip install chromadb ollama pypdf langchain-text-splitters

# 3. Pull Sovereign Models
ollama pull nomic-embed-text
ollama pull llama3.2:1b

# 4. Verify Document Presence
ls -F data/
# Expected: corporate_policy.pdf
```

---

## 🛠️ 2. Step-by-Step Execution
Follow these commands to build and query your knowledge vault.

### Phase A: Knowledge Ingestion
We will chunk our policy document and index it into ChromaDB.

```bash
# Execute the Vault Builder
python3 logic/vault_builder.py
```

### Phase B: Query Verification
The script will automatically perform a test query. Confirm the grounded response based on the policy context.

```bash
# Verify the persistent Chroma indices
ls -d chroma_db/
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Local RAG semantic search.*

Successfully running `vault_builder.py` retrieves specific clauses. Below is your target proof:
```text
[3/3] Indexing in ChromaDB...
✅ Vault updated with 3 entries.

--- QUERYING VAULT: What is the maximum limit for technology expenses? ---

[RETRIEVED CONTEXT]
Clause 1: TECHNOLOGY: All server expenses must be approved if over $10,000.

[SOVEREIGN ANSWER]
The maximum limit for technology expenses requiring standard manager approval is $10,000.
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Groundedness and Data Sovereignty.*

As an Architect, you ensure the model only answers from the **Retrieved Context**.

```python
# ARCHITECT EVIDENCE: Groundedness Prompt
prompt = f"Using ONLY the following context, answer the question: {context}\n\nQuestion: {question}"
```
Target Result:
```text
✅ ChromaDB Persistence: Verified.
✅ Local Execution: 100% (No external API calls used).
```
