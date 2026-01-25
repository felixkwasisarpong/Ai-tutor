# 🎓 Canon — Agentic RAG Academic Correctness & Citation-First AI Platform

![Canon Banner](docs/banner.png)

> **A production-grade, agentic, course-aware AI academic platform for university-level sciences — combining Retrieval-Augmented Generation (RAG), LangGraph-based decision logic, structured academic data models, and local LLM inference.**

---

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-purple)
![RAG](https://img.shields.io/badge/RAG-Course_Aware-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-lightgrey)
![Postgres](https://img.shields.io/badge/Postgres-Relational_DB-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Status](https://img.shields.io/badge/status-active_development-success)

---

⭐ **Star this repository** — your support helps guide future development!

---

## 🔥 Why Canon?

**Canon is not a generic chatbot or tutor.**  
It is an **academic correctness and citation-first AI backend** designed for real university-level academic environments.

Unlike chatbots that guess, Canon:
- Enforces **course-grounded answers**
- Uses **official course documents**
- Applies **deterministic routing policies**
- Separates **admin data control** from student usage

This dramatically reduces hallucinations and enforces academic integrity.

---

## 🧠 About

Canon is an **agentic backend** built to support **Computer Science, Engineering, Physics, and Information Theory** courses.

It combines:
- A structured **University-style data model**
- **Admin-controlled ingestion** of course materials
- **Metadata-aware RAG**
- **Local LLM inference** (no external APIs)

The result is **accurate, explainable, auditable, and citation-aware AI academic assistance**.

---

## ✨ Key Features

### 🤖 Agentic Decision Layer (LangGraph)
- LLM-powered intent routing
- Hard policy overrides (course references force RAG)
- Explicit reasoning paths (RAG vs direct LLM)

### 🏛️ Academic Data Model (Production-Grade)
- **Departments**
- **Courses**
- **Documents**
- Enforced via **PostgreSQL + foreign keys**
- No magic registries or hardcoded mappings

### 📄 Course-Aware RAG
- PDF ingestion with metadata:
  - department
  - course code
  - document title
  - chunk index
- Persistent FAISS vector store
- Deterministic retrieval filtering

### 🧠 Local LLM Inference
- Ollama-powered local models (e.g. `llama3`)
- Fully Dockerized
- No external API dependency

### 🔐 Admin Security Model
- Admin-only endpoints protected by API key
- Separation of concerns:
  - Admins manage data
  - Students ask questions

### 🧾 Citation-Aware Answers
- Responses include:
  - document title
  - chunk index
- Transparent grounding of answers

### 🧪 Confidence-Gated Academic RAG
- Confidence levels (high / medium / low / none)
- Refusal to answer when course material is insufficient
- Partial-confidence follow-up hints
- Hallucination prevention by design

### 📚 Versioned & Auditable Course Documents
- Document versioning (no silent overwrites)
- Active/inactive document enforcement
- Deterministic retrieval from latest official material
- Audit-friendly academic data governance

---

## 🏗️ System Architecture

```text
┌────────────┐
│  Student   │
└─────┬──────┘
      │ Question
      ▼
┌──────────────┐
│ FastAPI API  │
└─────┬────────┘
      ▼
┌─────────────────────────┐
│ Agent (LangGraph)       │
│  - Intent Classification│
│  - Policy Enforcement   │
└─────┬───────────┬───────┘
      │           │
      ▼           ▼
 Course RAG     Direct LLM
      │           │
      ▼           ▼
FAISS + PDFs   Ollama (Local)
```

---

## 🔄 How It Works

1. A student submits a question
2. The agent evaluates intent and routing rules
3. Course references **force RAG**
4. Documents are filtered by course metadata
5. Confidence is computed from retrieved material and enforced by the agent.
6. The LLM generates a grounded response
7. Citations are returned with the answer

---

## 🗃️ Database Schema (Core)

- **departments**
- **courses**
  - FK → departments
- **documents**
  - FK → courses

All schema changes are managed via **Alembic migrations**  
No automatic data seeding in production.

---

## 🔐 Admin Endpoints (Protected)

All admin endpoints require:

```
X-Admin-Key: <ADMIN_API_KEY>
```

### Admin capabilities:
- Create departments
- Create courses
- Upload course documents (PDFs)

### Public endpoints:
- `/ask` — student-facing question answering

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── api/            # FastAPI routes (admin + public)
│   ├── agent/          # LangGraph agent logic
│   ├── llm/            # Ollama client & generation
│   ├── rag/            # Ingestion, retrieval, vector store
│   ├── db/             # SQLAlchemy models & sessions
│   ├── services/       # Business logic
│   └── core/           # Config & auth
├── data/               # Uploaded PDFs
├── rag_store/          # Persistent FAISS index
├── alembic/            # DB migrations
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

### Pull LLM model (inside container)

```bash
docker compose exec ollama ollama pull llama3
```

---

## 📖 Example API Usage

### Ask a question

```http
POST /ask
```

```json
{
  "question": "Explain entropy as used in this course",
  "course_code": "CS5589"
}
```

### Response (example)

```json
{
  "answer": "...",
  "source": "rag:CS5589",
  "citations": [
    {
      "document": "Lecture 3 – Entropy",
      "chunk": 14
    }
  ]
}
```

---


## 🛡️ Platform Hardening (Phase 5)

Canon has completed a full platform-hardening phase focused on production readiness and academic integrity.

This phase includes:
- **Observability**: request IDs, structured logging, health and readiness checks, and admin audit logs
- **Inference robustness**: agentic routing, confidence-gated RAG, and explicit refusal policies
- **Security boundaries**: admin-only authentication for academic data control
- **UX planning**: finalized student and admin interaction flows with stable API contracts

Phase 5 intentionally prioritizes correctness, traceability, and operational safety over feature velocity.

## 🛣️ Roadmap

### ✅ Completed
- Agentic routing (LangGraph)
- Course-aware RAG
- Persistent vector store
- Admin auth guard
- PostgreSQL-backed university schema
- Citation-aware responses
- Local LLM inference (Ollama)
- Confidence-based clarification
- Document versioning and supersession

### 🔜 Planned
- Admin UI
- Student UI
- Streaming responses
- AWS deployment (Terraform + ECS + RDS)

---

## 🤝 Support

If you find this project useful:
- ⭐ Star the repository
- 🧠 Use it in your course
- 🚀 Extend it to new subjects