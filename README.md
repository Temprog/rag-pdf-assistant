# AI Banking Regulations Assistant (RAG System)

A Retrieval-Augmented Generation (RAG) system designed to answer questions on UK financial regulatory documents using AI.

Designed and implemented an AI-powered Retrieval-Augmented Generation (RAG) system for querying UK financial regulatory documentation, delivering explainable responses with source traceability, evaluation metrics, audit logging and safety guardrails for regulated-environment use cases.

---

## 🚀 Overview

- Ingested FCA Operational Resilience guidance from PDF documents and transformed content into searchable vector embeddings.
- Built a semantic retrieval pipeline using ChromaDB and embedding models to identify the most relevant regulatory context for user queries.
- Implemented Retrieval-Augmented Generation (RAG) to generate grounded responses from retrieved source material rather than relying solely on model knowledge.
- Added page-level citations to improve explainability and support traceability of generated answers.
- Incorporated retrieval evaluation scoring to assess alignment between user queries and retrieved context.
- Implemented audit logging and safety guardrails to support responsible AI practices within regulated environments.
- Developed an interactive Streamlit interface supporting configurable OpenAI and HuggingFace embedding backends.

--

## 🚀 Features

- 📄 PDF ingestion (FCA Operational Resilience guidance)
- 🔍 Semantic search using embeddings
- 🧠 RAG-based answer generation
- 📊 Retrieval quality evaluation scoring
- 📌 Page-level citations for transparency
- 🧾 Audit logging (banking-style traceability)
- 🛡️ Basic safety guardrails
- 💾 Persistent vector database (no recomputation)
- 🔄 Dual-mode embeddings (OpenAI or HuggingFace)

---

## 🏗️ Architecture

User Query → Streamlit UI → Embedding Model → Vector DB (Chroma) → Retrieval → LLM → Answer + Citations + Score

---

## 🧠 Tech Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- OpenAI GPT-4o-mini (optional)
- HuggingFace sentence-transformers
- PyPDF

---

## 🔁 Modes

### Free Mode (Default)
- HuggingFace embeddings
- No API cost
- Fully local retrieval

### Premium Mode
- OpenAI embeddings + GPT model
- Higher accuracy responses

---

## 📊 Evaluation System

Each query includes:

- Cosine similarity score between query and retrieved documents
- Displays retrieval confidence in UI

---

## 📌 Citations

Each answer includes:
- Source document chunk
- Page number from PDF
- Extracted context preview

---

## 🧾 Audit Logging

All interactions are stored in:

audit_log.json

---


Each record contains:
- timestamp
- question
- answer
- retrieval score

---

## 🧠 Safety Features

- Basic query filtering for unsafe terms
- Prevents restricted or malicious prompts

---

## 🏛️ Use Case

Designed for:
- Regulatory assistants
- Compliance research tools
- Banking AI copilots
- Internal knowledge assistants

---

## 🏗️ Architecture Diagram



                    ┌────────────────────────────┐
                    │        User Query          │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │      Streamlit UI          │
                    │        (app.py)            │
                    └────────────┬───────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │         Safety Guardrails (optional)       │
        │   - block unsafe / irrelevant queries      │
        └────────────┬───────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │   Embedding Model         │
                    │  (OpenAI or HuggingFace)  │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │   Vector Database          │
                    │       ChromaDB             │
                    │ (persistent cache store)   │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │  Top-K Document Retrieval  │
                    │  (semantic similarity)     │
                    └────────────┬───────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │     Evaluation Layer (Cosine Score)        │
        │   measures query ↔ document relevance      │
        └────────────┬───────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │     LLM (GPT-4o-mini)      │
                    │  grounded answer generation │
                    └────────────┬───────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │   Output Layer (Streamlit UI)              │
        │  - Final Answer                            │
        │  - Page Citations                         │
        │  - Retrieval Score                        │
        │  - Retrieved Context                      │
        └────────────┬───────────────────────────────┘
                                 │
                                 ▼
        ┌────────────────────────────────────────────┐
        │       Audit Logging System                 │
        │  (timestamp, question, answer, score)      │
        └────────────────────────────────────────────┘

---

## 🛠️ Tech Stack

- Python, Streamlit, LangChain, ChromaDB, OpenAI, HuggingFace Embeddings, Vector Databases, RAG, Prompt Engineering, PDF Processing, Generative AI.

---

## ⚠️ Known Issue

There is a known compatibility issue with ChromaDB on Python 3.14:

- Error: `RustBindingsAPI has no attribute 'bindings'`

### Fix
Run the project using Python 3.11 or 3.12:

```bash
python3.11 -m venv venv
pip install -r requirements.txt



