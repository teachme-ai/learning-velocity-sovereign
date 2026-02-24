# Session 04: Sovereign Knowledge RAG

## Overview
This session explores the architecture of **Retrieval-Augmented Generation (RAG)** within a sovereign enterprise context. We focus on converting unstructured documents into searchable vector embeddings and implementing a local RAG pipeline that ensures data never leaves the corporate perimeter while maintaining high factual accuracy.

## Learning Outcomes
- [ ] **LO1**: Understand Vector Embeddings and Semantic Search.
- [ ] **LO2**: Build a local RAG pipeline using ChromaDB or Qdrant.
- [ ] **LO3**: Mitigate hallucinations through "Groundedness" checks.

## [INTEGRATOR] Lab
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
