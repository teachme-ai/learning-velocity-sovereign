# Lab 04: Sovereign Knowledge (RAG)
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Modern AI models are powerful, but they lack awareness of *your* internal company documents. In this lab, we build a **Sovereign Knowledge Base** using Retrieval-Augmented Generation (RAG). 

You will construct a pipeline that ingests a corporate travel policy, generates local mathematical representations (embeddings) using Ollama, and securely stores them in a local FAISS vector database. Finally, we query this local database to answer policy questions definitively without sending data to the cloud.

---

## ⚙️ 1. Environment Setup

Copy and paste this block to prepare your RAG environment.

```bash
# 1. Ensure the directories exist
mkdir -p 04_sovereign_knowledge_rag/data
mkdir -p 04_sovereign_knowledge_rag/logic

# 2. View the Dummy Travel Policy
cat 04_sovereign_knowledge_rag/data/travel_policy.txt

# 3. View the Langchain Injection Script
cat 04_sovereign_knowledge_rag/logic/ingest_and_query.py

# 4. Verify Local Models are available
curl -s http://localhost:11434/api/tags | grep nomic-embed-text
```

---

## 🛠️ 2. Step-by-Step Execution

Follow these commands to launch the data pipeline.

### Phase A: Ingestion and Vector Search
Execute the script to load the text, generate embeddings on your local GPU, store them in the `db/` folder, and perform an automated query.

```bash
# Run the RAG workflow
python3 04_sovereign_knowledge_rag/logic/ingest_and_query.py
```

### Phase B: Verification
Confirm that the vector store was successfully created.

```bash
# Look for the FAISS database index files
ls -l 04_sovereign_knowledge_rag/db/
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Local Vectorization and Retrieval.*

A successful execution confirms the policy document was ingested and queried. Below is your target terminal proof:

```text
--- Sovereign Knowledge: RAG Pipeline ---
[STEP 1] Loading document...
 [OK] Loaded 1 document(s).
 [OK] Split into 3 chunks.
[STEP 2] Generating Local Embeddings & Storing with FAISS...
 [OK] Vector store initialized at /db.

[STEP 3] Executing Query: 'What is the limit for daily meal expenses?'

--- AI Response ---
Based on the provided context, the limit for daily meal expenses is $50 per day for domestic travel and $75 per day for international travel.

--- Pipeline Complete ---
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Embedding Modality and Local LLM Chaining.*

The true sovereign power lies in the LangChain orchestration.

```python
# ARCHITECT EVIDENCE: Local Embedding Engine
# Use Nomic Embeddings from local Ollama
embeddings = OllamaEmbeddings(
    model="nomic-embed-text:latest",
    base_url="http://localhost:11434"
)

# ARCHITECT EVIDENCE: Local Generation Engine
# Use Qwen or Llama 3.2 for the generation step
llm = OllamaLLM(
    model="llama3.2:1b",
    base_url="http://localhost:11434",
    temperature=0
)
```

**Target Result**:
By verifying these imports and instantiation blocks, we mathematically prove that both the initial vectorization and final sequence generation never left the host machine.
