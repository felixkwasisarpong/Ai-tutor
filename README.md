
# 🎓 AI Tutor — Agentic RAG Learning Assistant

![AI Tutor Banner](docs/banner.jpg)

> **An agentic, course-aware AI tutor for university-level sciences, combining Retrieval-Augmented Generation (RAG), LangGraph-based decision logic, and local LLM inference.**

---

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-purple)
![RAG](https://img.shields.io/badge/RAG-Metadata_Aware-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-lightgrey)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Status](https://img.shields.io/badge/status-active_development-success)

---

⭐ **Star this repository** — your support helps guide future development!

---

## 🔥 Why AI Tutor?

AI Tutor is **not a generic chatbot**. It is a **teaching-first AI system** that understands *when* to answer from general knowledge and *when* to ground responses in official course materials.

Key goals:
- Reduce hallucinations in academic settings
- Enforce course-grounded answers when required
- Support university-level science learning

---

## 📚 Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [RAG & Agent Logic](#rag--agent-logic)
- [Roadmap](#roadmap)

---

## 🧠 About

**AI Tutor** is an agentic backend designed to support **Physics, Information Theory, Machine Learning, and Engineering** courses.

It uses:
- Deterministic routing policies
- Metadata-aware document retrieval
- Local LLM inference via Ollama

This ensures answers are **accurate, contextual, and pedagogically aligned**.

---

## ✨ Key Features

### 🤖 Agentic Decision Layer
- Built with **LangGraph**
- LLM-powered routing with hard policy overrides
- Explicit detection of course-referencing language

### 📄 Multi-Document RAG
- PDF ingestion with metadata (course, document)
- Persistent FAISS vector store
- Metadata-aware retrieval and filtering

### 🧠 Local LLM Inference
- Ollama-powered local models
- Fully Dockerized
- No external API dependency

### 🧱 Production-Ready Backend
- FastAPI REST API
- Docker Compose orchestration
- Persistent vector storage
- Designed for AWS ECS/Fargate (Terraform planned)

---

## 🏗️ System Architecture

```text
┌────────────┐
│   Student  │
└─────┬──────┘
      │ Question
      ▼
┌──────────────┐
│ FastAPI API  │
└─────┬────────┘
      ▼
┌─────────────────────┐
│ Agent (LangGraph)   │
│  - Intent Routing   │
│  - Policy Overrides │
└─────┬───────────────┘
      │
 ┌────┴─────┐
 │          │
 ▼          ▼
RAG       Direct LLM
 │          │
 ▼          ▼
FAISS     Ollama
(PDFs)    (Local)
```

---

## 🔄 How It Works

1. A student submits a question
2. The agent evaluates intent and policy rules
3. Course references force RAG retrieval
4. Metadata filters relevant documents
5. The LLM generates a grounded response
6. Safe fallback on uncertainty

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── api/            # FastAPI routes
│   ├── agent/          # LangGraph logic
│   ├── llm/            # Ollama client
│   ├── rag/            # Ingestion & retrieval
│   └── core/           # Configuration
├── data/               # Course PDFs
├── rag_store/          # Persistent FAISS index
├── docker-compose.yml
└── Dockerfile
```

---

## 🧪 Local Development

### Prerequisites
- Docker
- Docker Compose
- ~8GB RAM recommended for local LLM inference

### Run locally

```bash
docker compose up --build
```

### Example API Request

```http
POST /ask
```

```json
{
  "question": "Explain entropy as used in this course"
}
```

---

## 📖 RAG & Agent Logic

### RAG is **forced** when:
- "this course"
- "according to the notes"
- "from the lecture"
- "in class"

### RAG is **skipped** when:
- The question is general knowledge
- No explicit course reference exists

This ensures **teaching accuracy over convenience**.

---

## 🛣️ Roadmap

### ✅ Completed
- Agentic routing
- Multi-document RAG
- Metadata-aware retrieval
- Local LLM inference
- Persistent vector store

### 🔜 Planned
- Confidence-based clarification
- Citation-aware responses
- Streaming answers
- AWS deployment via Terraform

---

## 🤝 Support

If you find this project useful:
- ⭐ Star the repository
- 🧠 Use it in your course
- 🚀 Extend it to new subjects
