# Lab 04: Sovereign Knowledge RAG — The Local Vault
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
In this final lab, you build the **Sovereign Knowledge RAG** pipeline. You will ingest the 2026 Corporate Policy into a local vector store (ChromaDB) and use a local embedding model (Ollama) to perform semantically grounded queries via Gemini.

---

## ⚙️ 1. Environment Setup
Standardize your environment with these core RAG dependencies.

```bash
# 1. Install RAG Stack
pip install chromadb ollama google-generativeai langchain pypdf

# 2. Pull Embedding Model
ollama pull nomic-embed-text
```

---

## 🛠️ 2. Step-by-Step Execution

### Phase A: Ingestion & Vectorization
We will transform the markdown policy into a persistent vector database.

```bash
# Execute the Vault Manager (Ingests & Tests)
python3 logic/vault_manager.py
```

### Phase B: Groundedness Test
The system is designed to refuse answers not explicitly found in the vault.

```bash
# Verify 'I do not have the authority' response for:
# "Can I get a subscription for Netflix?"
```

---

## 🏗️ [INTEGRATOR / ARCHITECT] Evidence

### 🔒 Ingestion Success
```text
[1/3] Reading policy from corporate_policy_2026.md...
[2/3] Chunking text...
[3/3] Indexing in ChromaDB...
✅ Vault updated with 4 entries.
```

### 🎯 Groundedness Proof
```text
--- QUERY: Can I get a subscription for Netflix? ---
[VAULT CONTEXT]: AI Tooling & Subscriptions... Individual LLM subscriptions...

[SOVEREIGN RESPONSE]:
I do not have the authority to answer based on current policy.
```
