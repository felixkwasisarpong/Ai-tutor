# 🎓 Canon — Agentic RAG Academic Correctness & Citation-First AI Platform

![Canon Banner](docs/banner.png)

> **A production-grade, agentic, course-aware AI academic platform for university-level sciences — combining Retrieval-Augmented Generation (RAG), LangGraph-based decision logic, structured academic data models, and local LLM inference. Now fully deployed on AWS infrastructure for scalable, secure, and reliable academic assistance.**

---

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-purple)
![RAG](https://img.shields.io/badge/RAG-Course_Aware-orange)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-lightgrey)
![Postgres](https://img.shields.io/badge/Postgres-Relational_DB-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![AWS](https://img.shields.io/badge/AWS-Cloud_Deployment-yellowgreen)
![Status](https://img.shields.io/badge/status-production_success-brightgreen)

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

## 🚀 Deployment Status (Production)

Canon is fully deployed and production-ready, leveraging AWS cloud infrastructure to ensure scalability, security, and high availability:

- Backend hosted on **AWS ECS Fargate**, running containerized FastAPI services behind an **Application Load Balancer (ALB)**
- **PostgreSQL database managed on AWS RDS** for reliable and scalable data storage
- Sensitive configuration and credentials managed securely via **AWS Secrets Manager**
- Frontend UI hosted on **AWS S3** with global distribution through **CloudFront CDN**
- Continuous Integration and Deployment (CI/CD) pipelines implemented via **GitHub Actions** for automated testing and deployment

---

## 🔧 Infrastructure

The entire cloud infrastructure for Canon is managed through **Terraform**, enabling consistent, version-controlled provisioning of:

- ECS Fargate clusters and services
- ALB and target groups
- RDS PostgreSQL instances with automated backups
- S3 buckets and CloudFront distributions for frontend hosting
- IAM roles and policies for secure resource access
- Secrets Manager secrets for sensitive data management

This infrastructure-as-code approach ensures reproducibility, auditability, and ease of maintenance.

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

### 🔁 Policy-Gated Follow-Up Questions
- Follow-up prompts emitted explicitly by the agent (not free-form chat)
- Triggered only for low / medium confidence answers
- Follow-ups treated as fresh academic queries
- Prevents conversational drift and citation bypass

### 🧠 Bounded Conversation Memory
- Short-lived, per-request academic memory
- Used only to support explicit follow-up questions
- Time- and size-bounded to prevent hallucination drift
- Never treated as ground truth or cited material

### 🧩 Multi-Modal Question Normalization
- Supports text + PDF supplementary context
- OCR scaffolding for images (exam-style diagrams, notes)
- Modality-aware agent routing
- Preserves citation and confidence guarantees

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
5. Confidence is computed deterministically and follow-up eligibility is evaluated  
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

## 🔑 Authentication & Roles

Canon uses JWT-based authentication with distinct roles for students and admins. Access tokens are issued as JWTs, enabling stateless and secure API access. Refresh tokens support session renewal and token revocation to maintain security.

- **JWT Access Tokens:** Short-lived tokens granting access to protected endpoints.  
- **Refresh Tokens:** Used to obtain new access tokens without re-authentication; revocable for security.  
- **Roles:** Student and Admin roles are enforced to separate permissions; admins manage data ingestion and configuration, while students access question answering features.  
- **API Protection:** Admin endpoints require valid JWTs with admin role claims; student endpoints require student role tokens. This ensures strict access control and auditability.

---

## 🖥️ User Interfaces

Canon provides dedicated web UIs for both students and admins, built with Next.js and tightly integrated with the backend via a well-defined API contract.

- **Student UI:**  
  - Login and authentication flows  
  - Submit academic questions with course context  
  - View answers with citations and confidence levels  
  - Engage in policy-gated follow-ups  
  - Support for multi-modal inputs including PDFs and images with OCR  

- **Admin UI:**  
  - Manage departments, courses, and course documents  
  - Upload and version academic PDFs  
  - Monitor ingestion and data status  
  - Role-based access control with audit trails  

The UI communicates through a stable, versioned API ensuring smooth interaction and future extensibility.

---

## 🛣️ Roadmap (Updated)

### ✅ Completed
- Agentic routing (LangGraph)  
- Course-aware RAG  
- Persistent vector store  
- Admin auth guard  
- PostgreSQL-backed university schema  
- Citation-aware responses  
- Local LLM inference (Ollama)  
- Confidence-gated answers (high / medium / low / none)  
- Policy-gated follow-up questions  
- Bounded conversation memory (TTL-based)  
- Multi-modal input normalization (text + PDF)  
- Observability (request IDs, structured logging)  
- JWT-based authentication (student + admin roles)  
- Refresh tokens & token revocation  
- Student UI (Next.js): login, ask question, citations, confidence, follow-ups  
- Admin UI: department/course/document management  
- UI CI (lint + build)  
- Follow-up question UX  
- Multi-modal input scaffolding (PDF, image OCR)  
- Live audio input (speech-to-text)  
- OCR backend integration finalization  
- **AWS deployment: Terraform + ECS + ALB + RDS**  
- **CloudFront + S3 UI hosting**  
- **Cost controls & budgets**


---

## 🧪 Operational Guarantees

Canon enforces strict operational guarantees to maintain academic integrity and reliability:

- No hallucinations without explicit citations to course materials  
- Refusal policy for insufficient or out-of-scope content  
- Bounded conversation memory preventing drift and misinformation  
- Transparent confidence scoring and policy-driven follow-ups  

---

## 📌 Status

**Production-deployed, actively maintained.**

---

## 🤝 Support

If you find this project useful:  
- ⭐ Star the repository  
- 🧠 Use it in your course  
- 🚀 Extend it to new subjects