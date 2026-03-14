# Session 04: Sovereign Knowledge RAG

## Overview
This session explores the architecture of **Retrieval-Augmented Generation (RAG)** within a sovereign enterprise context, focusing on converting unstructured documents into searchable vector embeddings while maintaining high factual accuracy. We will delve into how to implement a local RAG pipeline using ChromaDB or Qdrant and mitigate hallucinations through "Groundedness" checks.

## Learning Outcomes
- **LO1**: Understand Vector Embeddings and Semantic Search.
- **LO2**: Build a local RAG pipeline using ChromaDB or Qdrant.
- **LO3**: Mitigate hallucinations through "Groundedness" checks.

## [INTEGRATOR] Lab

### The Lesson: Semantic vs. Keyword Search
In traditional keyword search, the computer looks for exact words in documents. However, this approach is limited to matching specific keywords rather than understanding the actual intent of the text. **Semantic Search**, on the other hand, uses vector embeddings to understand the meaning behind the words and retrieve relevant information.

### The Tool: NotebookLM vs. Sovereign Vault

- **NotebookLM**: A powerful tool that automatically handles semantic search in the cloud. It is ideal for personal research but provides a great foundation for developers.
- **Sovereign Vault**: Our local ChromaDB implementation gives the enterprise full control over the data, embedding model, and retrieval logic.

### Tasks
- **Local Vector Store**: Set up a local ChromaDB instance or use a file-based Qdrant store to store vector embeddings of technical policy documents.
- **Document Ingestion**: Implement a script to chunk and embed PDFs of relevant documents in the policy library.
- **Semantic Query**: Connect NotebookLM to the vector store to answer domain-specific questions.

## [ARCHITECT] Lab
- **Embedding Analysis**: Compare different embedding models (e.g., Nomic vs. OpenAI) via local benchmarks for optimal performance in semantic search scenarios.
- **Reranking Logic**: Implement a cross-encoder reranker to improve retrieval precision, ensuring that retrieved results accurately reflect the actual intent of the text.
- **Groundedness Logic**: Design an "Expert" agent that verifies if LLM answers are explicitly supported by retrieved chunks and flags any inconsistencies.

## Governance Notes
- **Data Sovereignty**: All embeddings and vector indices are stored locally to ensure data sovereignty and prevent vendor lock-in or IP leaks.
- **Auditability**: Each AI response must include citations to the specific document chunks used in the retrieval phase, ensuring auditability and compliance with regulations.