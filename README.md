# SentinelRAG
**Enterprise-Grade Secure Knowledge Intelligence Platform**

## Short Description
A production-grade, secure, role-based Retrieval-Augmented Generation (RAG) platform for internal enterprise knowledge systems. Features include RBAC enforcement, semantic caching, parent–child document retrieval, evaluation pipelines, and cloud-native deployment on Azure.


## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Capabilities](#key-capabilities)
- [Project Value & Use Case](#-project-value--use-case)
- [System Architecture (High-Level)](#system-architecture-high-level)
- [Security Model](#security-model)
- [Evaluation & Benchmarking](#evaluation--benchmarking)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Running Locally](#running-locally)
- [Deployment](#deployment)

---
## Problem Statement

Modern enterprises store vast internal knowledge (HR policies, payroll, compliance, guidelines, procedures) across fragmented systems such as PDFs, shared drives, portals, and repositories.

As organizations scale, they face critical issues:

- **Knowledge Fragmentation**  
  Information is scattered across disconnected systems, making it hard to find accurate and authoritative answers quickly.

- **Access Control Gaps**  
  Different roles (employee, manager, HR) require different access levels, but existing systems fail to enforce fine-grained, role-based access at the data level, leading to unauthorized exposure risks.

- **Ineffective Retrieval**  
  Keyword-based search lacks semantic understanding, producing irrelevant results and poor precision.

- **Lack of Context Awareness**  
  Systems cannot understand user intent, conversation history, or multi-turn queries, resulting in repetitive and inefficient interactions.

- **Security & Compliance Risks**  
  Weak access enforcement leads to data leakage, policy violations, and compliance failures involving confidential information.

- **Operational Inefficiency**  
  Employees waste significant time searching for information, directly reducing productivity and efficiency.

- **Unreliable AI Systems**  
  Existing AI assistants lack evaluation, benchmarking, and validation mechanisms, making them unmeasurable and untrustworthy for enterprise use.

---

### Core Problem Summary
Enterprises lack a secure, intelligent, and role-aware internal knowledge system that enforces data-level access control, enables semantic and context-aware multi-turn retrieval, prevents unauthorized data exposure, delivers accurate and grounded answers, and operates with measurable reliability at production scale.

# Solution Overview

The solution is a secure, enterprise-grade internal knowledge platform that converts fragmented organizational documents into a centralized, role-aware knowledge layer accessible via natural language queries.

Built on a Retrieval-Augmented Generation (RAG) architecture, the system provides semantic, context-aware retrieval while enforcing strict data-level role-based access control. All responses are grounded in authorized internal documents, ensuring accuracy, security, and trust.

The platform supports multi-turn conversational interactions, delivers low-latency performance through optimized retrieval and caching, and includes evaluation and benchmarking mechanisms to ensure measurable reliability at production scale.

---

# Key Capabilities

### 🔐 Secure Internal Knowledge Access
- Controlled, authenticated access to internal organizational documents  
- Protected API layer with secure authorization flow  
- Enterprise-grade access isolation

---

### 🧭 Role-Based Access Control (RBAC)
Strict role enforcement across the entire pipeline:
- **Data layer**
- **Retrieval layer**
- **Cache layer**
- **Response generation layer**

**Roles supported:**  
- Employee  
- Manager  
- HR  

➡ Prevents unauthorized access and information leakage end-to-end.

---

### 🧠 Semantic Knowledge Retrieval
- Embedding-based semantic search
- Intent understanding beyond keyword matching
- Context-aware information discovery
- High-precision, relevance-driven responses

---

### 🔀 Hybrid Retrieval Architecture
Combination of:
- **Dense vector search** (semantic similarity)
- **Sparse retrieval** (keyword precision)

➡ Improved recall, precision, and result quality.

---

### 🧱 Hierarchical Document Modeling
- Parent–child document structure
- Context preservation
- Structural coherence
- Logical segmentation of knowledge

➡ Better contextual grounding and answer accuracy.

---

### 💬 Context-Aware Conversational Memory
Supports natural multi-turn conversations using:
- Session memory
- Query summarization
- Context condensation
- Conversation state tracking

➡ Human-like internal knowledge interaction.

---

### ⚡ Role-Isolated Semantic Caching
High-performance caching with:
- Role-scoped cache keys
- Semantic similarity matching
- Cross-role data isolation
- Zero data leakage guarantee

➡ Faster responses + strict security.

---

### 🛡️ Enterprise-Grade Security Model
Security-first architecture including:
- JWT authentication
- RBAC enforcement
- Role-based filtering
- Secure secret management
- Token-based authorization
- API protection layers

---

### 🚄 Performance-Optimized Pipeline
Latency-optimized system using:
- Multi-layer caching
- Retrieval optimization
- Threshold-based reranking
- Resource-aware processing
- Query filtering pipelines

➡ Fast, scalable, and cost-efficient performance.

---

### 📊 Evaluation & Benchmarking Framework
Built-in evaluation pipelines for:
- Latency measurement
- Retrieval accuracy
- RBAC validation
- Security testing
- Response quality assessment
- Generation reliability

---

### ☁️ Cloud-Native Deployment
Designed for modern infrastructure:
- Containerized architecture
- Environment-based configuration
- Secure secret injection
- Cloud portability
- CI/CD compatibility

---

### 🏗️ Production-Ready Architecture
Enterprise-grade system design with:
- Modular components
- Fault tolerance
- Graceful degradation
- Scalable services
- Clean separation of concerns
- Industry-grade deployment practices

---

✨ *Designed as an enterprise-grade, production-ready internal knowledge intelligence system — not just a chatbot.*

# Project Value & Use Case

This project demonstrates how an internal enterprise-grade AI system can:

- Reduce manual document search effort
- Improve internal knowledge accessibility
- Enable fast employee onboarding
- Reduce dependency on HR/helpdesk teams
- Improve compliance knowledge discovery
- Centralize organizational knowledge
- Provide secure role-based information access

# System Architecture (High-Level)

The system is designed as a **secure, layered enterprise platform** for internal knowledge access, intelligence, and controlled information delivery.

<details>
<summary><strong>📊 View System Architecture Diagram</strong></summary>

<br>

<p align="center">
  <img src="./docs/HLD/diagrams/architecture_overview.png" alt="Architecture Diagram" width="900"/>
</p>

</details> 
At a high level, the architecture is composed of the following logical layers:

---

## 👤 Client Layer
- Internal users  
- Internal applications  
- Admin tools  
- Enterprise services  

➡ All interactions occur through a secure API interface.

---

## 🔐 Secure API Layer
- Protected **FastAPI backend**
- Central request entry point
- Authentication handling
- Request validation
- Authorization enforcement
- API security controls

➡ Acts as the secure gateway to the entire system.

---

## 🆔 Identity & Access Layer
Security and access governance layer providing:
- JWT-based authentication
- Role-based access control (RBAC)
- Role validation
- Permission enforcement
- Access policy management

➡ Ensures users only access **authorized knowledge**.

---

## 📚 Knowledge Retrieval Layer
Intelligent knowledge access through:
- Semantic retrieval (vector embeddings)
- Hybrid search (dense + sparse)
- Intent understanding
- Relevance scoring
- Retrieval filtering

➡ Enables accurate and intelligent knowledge discovery.

---

## 🧱 Knowledge Structuring Layer
Document organization and context modeling using:
- Parent–child document hierarchy
- Structural segmentation
- Context boundaries
- Logical document grouping
- Hierarchical indexing

➡ Preserves document structure and contextual integrity.

---

## 🧠 AI Intelligence Layer
AI-driven reasoning and response generation:
- Context grounding
- Knowledge synthesis
- Hallucination control
- Answer coherence
- Context-aware generation

➡ Produces reliable, grounded, and accurate responses.

---

## ⚡ Caching & Memory Layer
Performance and conversation optimization via:
- Multi-layer caching
- Semantic cache
- Role-isolated cache
- Session memory
- Conversational state tracking
- Query summarization

➡ Enables fast responses and natural conversations.

---

## ☁️ Infrastructure Layer
Cloud-native operational foundation:
- Containerized deployment
- Secure configuration management
- Secret injection
- Environment isolation
- Scalable services
- CI/CD compatibility

➡ Production-grade, enterprise-ready infrastructure.

---

✨ *Architected as a secure, scalable, intelligent enterprise knowledge platform — not just a RAG system, but a full internal knowledge intelligence infrastructure.*




# Security Model

**Security is a core design principle of the system — not an afterthought.**

The platform is architected to ensure that internal organizational knowledge is accessed **only by authorized users**, under **strictly controlled, auditable, and enforceable conditions**.

---

## 🔑 Authentication
- **JWT-based Authentication**  
  - All protected API endpoints require JWT authentication  
  - Token-based session validation  

- **Organizational Credentials**  
  - Users authenticate using valid internal organizational credentials  

- **Bearer Token Enforcement**  
  - Every request must include a valid bearer token  
  - Unauthorized requests are automatically rejected  

---

## 🧭 Authorization (Role-Based Access Control – RBAC)
- **System-Wide RBAC Enforcement**  
  - RBAC is applied across **all layers**, not just APIs  

- **User Role Definitions**  
  - Roles supported:
    - `employee`  
    - `manager`  
    - `HR`  

- **Data-Level Authorization**  
  - Access control is enforced at the **data level**, not just at the interface level  

➡ Security is embedded in the data flow itself, not bolted on top.

---

## 🧱 Data-Level Role Isolation
- **Role-Access Tagging**  
  - Internal documents are tagged with role-based access metadata  

- **Role-Based Retrieval Filtering**  
  - Retrieval pipelines filter knowledge strictly by user role  

- **Unauthorized Content Prevention**  
  - Unauthorized documents are:
    - ❌ Never retrieved  
    - ❌ Never processed  
    - ❌ Never cached  
    - ❌ Never sent to AI models  
    - ❌ Never included in responses  

➡ Unauthorized data is structurally unreachable.

---

## 📚 Secure Knowledge Access
- **Authorized Content Only**  
  - Only permitted internal knowledge is used for answer generation  

- **Grounded AI Responses**  
  - All responses are grounded in authorized internal content  

- **No External Data Sources**  
  - No external APIs or public knowledge bases are used  

➡ Prevents hallucination, leakage, and data contamination.

---

## 🔒 Secure Configuration Management
- **No In-Code Secrets**  
  - No API keys, secrets, or credentials in source code  

- **Secure Secret Injection**  
  - Secrets injected via environment variables  

- **Cloud-Native Secret Management**  
  - Production uses cloud-native secret management systems  

➡ Zero hardcoded secrets policy.

---

## ⚡ Cache Security
- **Role-Isolated Semantic Cache**  
  - Cache keys are scoped by role  
  - Prevents cross-role data leakage  

- **Session-Scoped Memory**  
  - Memory is isolated per user session  

- **Consistent Access Control**  
  - Cached data follows the same RBAC rules as live retrieval  

➡ Cache layer is security-aware, not just performance-focused.

---

## ☁️ Infrastructure Security
- **Containerized Deployment**  
  - Environment isolation via containerization  

- **Cloud-Managed Security**  
  - Secure networking  
  - Runtime protection  
  - Managed infrastructure security services  

- **Restricted External Access**  
  - External service access limited strictly to required APIs  

➡ Production-grade infrastructure security model.

---

🛡️ **Security Philosophy**

> Security is enforced by **architecture**, not policy documents.  
> Unauthorized data is **structurally impossible to access**, not just logically restricted.

✨ *Designed as a zero-trust, enterprise-grade internal knowledge security architecture.*


---

# Evaluation & Benchmarking

The system is built as a measurable, validated, and benchmarked enterprise platform, with structured evaluation pipelines covering retrieval quality, generation quality, security enforcement, and performance.

---

## 🔍 Retrieval Evaluation (RAG Quality)
**Metrics:**
- **Recall@5**: 0.951
- **Precision@5**: 0.277
- **MRR**: 0.806
- **Total Queries Evaluated**: 226

This demonstrates high recall and ranking quality, ensuring relevant internal documents are consistently retrieved for answer generation.

## 🧠 Generation Quality Evaluation
**Metrics:**
- **Average Faithfulness**: 0.832
- **Average Answer Relevance**: 4.65 / 5

This validates that generated responses remain grounded in internal knowledge and are contextually relevant.

## ⚡ System Level Performance & Latency Benchmarking
**End-to-End Latency:**
- **P50**: 1.52s
- **P95**: 2.52s
- **P99**: 3.96s
- **Average**: 1.69s

**Component Latency (Avg):**
- **Embedding**: 0.32s
- **Retrieval**: 0.18s
- **Reranker**: 0.09s

## 💰 Cost Efficiency
**Average Cost Per Query:**
- **~ $0.00146 USD**

This demonstrates production-grade cost efficiency for enterprise-scale usage.

## 🔐 Security Validation (RBAC)
**RBAC Evaluation Results:**
- **Total Attack Tests**: 297
- **Violations Found**: 0
- **Violation Rate**: 0.0000

This confirms strict role isolation and zero unauthorized data access.

---

## Evaluation Summary

The system is not only functional, but:
- ✅ **Measured**
- ✅ **Benchmarked**
- ✅ **Validated**
- ✅ **Audited**
- ✅ **Security-tested**
- ✅ **Performance-tested**
- ✅ **Production-verified**


# Tech Stack

## Backend & API
- **Python** – Core programming language
- **FastAPI** – Secure, high-performance API framework
- **Uvicorn** – ASGI server for production execution

## AI & Machine Learning
- **OpenAI** – Embeddings for semantic retrieval
- **Groq** – LLM inference engine
- **Cohere** – Reranking model for retrieval optimization
- **LangChain** – Prompt orchestration and memory integration

## Retrieval & Knowledge Infrastructure
- **Pinecone** – Vector database for semantic search
- **BM25 Encoder** – Sparse retrieval for hybrid search
- **Parent–Child Chunking Model** – Hierarchical document structuring

## Caching & Memory
- **Redis** – Semantic cache and session memory backend

## Security & Access Control
- **JWT Authentication** – Secure user authentication
- **Role-Based Access Control (RBAC)** – Fine-grained permission management
- **Role-Isolated Semantic Caching** – Secure caching with role separation

## Evaluation & Benchmarking
- **Python Evaluation Scripts** – Custom assessment tools
- **Jupyter Notebooks** – Analysis and experimentation
- **Automated Benchmarking Pipelines** – Continuous performance monitoring

## DevOps & Deployment
- **Docker** – Containerization
- **Azure App Service** – Cloud deployment platform
- **GitHub Actions** – CI/CD pipeline automation

## Configuration & Secrets
- **Environment Variables** – Runtime configuration
- **Cloud Secret Injection** – Secure credential management

# Project Structure

The repository follows a modular, enterprise-oriented structure designed for scalability, maintainability, security, and clear separation of responsibilities:

# 📁 Project Structure

<details>
<summary><strong>📂 View Repository Structure</strong></summary>

<br>

```text
enterprise-internal-hr-knowledge-rag-main/
│
├── app/                             # Core application code
│   ├── auth/                        # Authentication & RBAC
│   │   ├── models.py                # Auth request/response models
│   │   ├── routes.py                # Login and auth APIs
│   │   └── users.py                 # User loading & RBAC data
│   │
│   ├── rag/                         # RAG pipeline & retrieval logic
│   │   ├── routes.py                # /ask and /ask_with_metrics APIs
│   │   ├── clients.py               # LLM, embeddings, retriever clients
│   │   └── parent_store.py          # Parent document storage
│   │
│   ├── cache/                       # Caching & memory layer
│   │   ├── memory.py                # Conversation memory & summarization
│   │   ├── semantic_cache.py        # Semantic caching logic
│   │   └── redis_client.py          # Redis connection handler
│   │
│   ├── core/                        # Core system services
│   │   ├── config.py                # Environment & secrets configuration
│   │   └── security.py              # JWT auth & security utilities
│   │
│   └── models/                      # Shared data models
│       └── query.py                 # Query request model
│
├── data/                            # Runtime system data
│   ├── users.xlsx                   # Internal user database
│   └── parent_chunks.jsonl          # Parent document store
│
├── eval_data/                       # Evaluation datasets
│   ├── generational_eval.jsonl
│   ├── latency_eval.jsonl
│   ├── retrieval_eval.jsonl
│   └── rbac_eval.jsonl
│
├── eval_scripts/                    # Evaluation execution scripts
│   ├── run_generation_eval.py
│   ├── run_latency_eval.py
│   ├── run_retrieval_eval.py
│   └── run_rbac_eval.py
│
├── evaluation/                      # Analysis, notebooks & reports
│   ├── generation_eval.ipynb
│   ├── latency_cost_eval.ipynb
│   ├── retrieval_eval.ipynb
│   ├── rbac_eval.ipynb
│   └── metrics_summary.md
│
├── notebooks/                       # Experimental & offline notebooks
│   └── multi_rag_pipeline.ipynb     # Ingestion pipeline Colab notebook
│                                     # (Used for document loading, chunking,
│                                     # hybrid encoding, embedding & vector DB ingestion)
│
├── ingestion/                       # Offline / batch ingestion pipeline
│   ├── config.py                    # Ingestion-specific configuration
│   ├── loader.py                    # Document loaders (PDF, DOCX, etc.)
│   ├── preprocessor.py              # Cleaning & normalization logic
│   ├── chunker.py                   # Text chunking strategies
│   ├── embedder.py                  # Embedding generation
│   ├── hybrid_encoder.py            # Sparse + dense encoding logic
│   ├── vector_store.py              # Vector DB insertion & indexing
│   └── pipeline.py                  # End-to-end ingestion orchestration
│
├── docs/                            # System documentation
│   ├── HLD/                         # High-Level Design
│   │   ├── hld.md                   # High-level system architecture
│   │   └── diagrams/               # Architecture & flow diagrams
│   │
│   └── lld.md                       # Low-Level Design (component-level details)
│
├── .github/workflows/               # CI/CD pipelines
│   └── docker-build.yml
│
├── Dockerfile                       # Container build configuration
├── .dockerignore                    # Docker build exclusions
├── .gitignore                       # Git version control exclusions
├── requirements.txt                 # Python dependencies
├── main.py                          # Application entry point
└── README.md                        # Project documentation

```
</details> 

# Running Locally

This section explains how to run the system in a local development environment for testing, development, and evaluation.

---

## Prerequisites
Ensure the following are installed:
- **Python 3.9+**
- **pip**
- **Redis** (local instance or cloud Redis)
- **Access to required API services:**
  - OpenAI
  - Groq
  - Pinecone
  - Cohere

## Step 1: Clone the Repository
```bash
git clone https://github.com/Tanish-analyst/enterprise-internal-hr-knowledge-rag.git
cd enterprise-internal-hr-knowledge-rag
```
### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a .env file in the root directory:
```bash
# Security
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Services
OPENAI_API_KEY=
GROQ_API_KEY=
COHERE_API_KEY=

# Retrieval
PINECONE_API_KEY=
PINECONE_INDEX=multi-rag-system

# Cache
REDIS_HOST=
REDIS_PORT=6379
REDIS_USERNAME=
REDIS_PASSWORD
```

### Step 5: Run the Application
``` bash
uvicorn main:app --reload
```
### Step 6: Access the API
- **API Base URL:**  
  `http://127.0.0.1:8000`
- **Interactive API Docs:**  
  `http://127.0.0.1:8000/docs`



#### Test User Credentials
For local testing and evaluation, user accounts are preloaded from: `data/users.xlsx`

This file contains 4000+ registered internal users with assigned roles:
- `employee`
- `manager`
- `hr`

  ---

#### Password Pattern (Testing Only)
For test users, the password format follows a deterministic pattern:

**Format:**
- **email:** `user<id>@company.com`
- **password:** `user<id>pass`

This pattern is used only for local testing and development.

# Deployment 
The system is designed for production-grade deployment using a containerized, cloud-native architecture.
**Core Characteristics:**
- Docker-based containerization
- Cloud-native deployment model
- Stateless API architecture
- Externalized configuration & secrets
- Secure secret injection
- CI/CD automation
- Infrastructure independence

**Cloud Model:**
- Containerized FastAPI service
- Cloud-managed runtime (Azure App Service)
- External AI services
- External vector database
- External cache backend

