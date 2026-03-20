# Session 04: Sovereign Knowledge RAG

## Overview
In the realm of AI for Cyber-Security, Retrieval-Augmented Generation (RAG) is a game-changer for incident response and threat hunting. Imagine having a digital equivalent of a forensics lab where you can query unstructured log files, network captures, or other sensitive data to extract relevant insights without compromising on security.

In this session, we'll delve into the architecture of RAG within a sovereign enterprise context. We'll focus on converting unstructured documents such as incident reports, system logs, or security dashboards into searchable vector embeddings using techniques like BERT and distilBERT. This allows us to build a local RAG pipeline that can analyze sensitive data without ever sending it out the corporate network.

Our goal is to strike a balance between high factual accuracy and operational efficiency. We'll explore trade-offs in model training, inference time, and data processing to ensure that our RAG pipeline meets the demands of real-world security operations.
## Learning Outcomes
- [ ] **LO1**: Understand Vector Embeddings and Semantic Search.
- [ ] **LO2**: Build a local RAG pipeline using ChromaDB or Qdrant.
- [ ] **LO3**: Mitigate hallucinations through "Groundedness" checks.

## [BUILDER] Lab

### The Lesson: Semantic vs. Keyword Search
Traditional **Keyword Search** is like looking for a needle in a haystack by matching colors. If you search for *"money for a hotel"*, the computer only looks for those exact words. If the policy uses the term *"Travel Reimbursement"*, a keyword search will fail.

**Semantic Search** (Vector Search) understands the **intent**. It knows that *"money for a hotel"* is semantically related to *"Travel Reimbursement"*. By converting text into mathematical vectors, we can find answers based on meaning, not just spelling.

### The Tool: NotebookLM vs. Sovereign Vault
- **NotebookLM**: A powerful tool that handles this automatically in the cloud. It's great for personal research but often hides the "how" from the developer.
- **Sovereign Vault**: Our local ChromaDB implementation gives the **Enterprise** full control. You decide which embedding model to use, where the data is stored, and exactly how the retrieval logic is tuned.

### Tasks
- **Local Vector Store**: Spin up a local ChromaDB instance or use a file-based Qdrant store.
- **Document Ingestion**: Implement a script to chunk and embed technical policy PDFs.
- **Semantic Query**: Connect a local LLM to the vector store to answer domain-specific questions.

## [ARCHITECT] Lab
- **Embedding Analysis**: Compare different embedding models (e.g., Nomic vs. OpenAI) via local benchmarks.
- **Reranking Logic**: Implement a cross-encoder reranker to improve retrieval precision.
- **Groundedness Logic**: Design a "Critic" agent that verifies if LLM answers are explicitly supported by retrieved chunks.

## Governance Notes
- **Data Sovereignty**: All embeddings and vector indices are stored locally to prevent vendor lock-in and IP leaks.
- **Auditability**: Every AI response must include citations to the specific document chunks used in the retrieval phase.