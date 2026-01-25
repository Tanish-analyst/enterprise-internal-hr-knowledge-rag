# 📘 Low-Level Design (LLD)
## Enterprise Internal HR Knowledge RAG System

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)  
2. [Module-Level Design](#2-module-Level-design)  
3. [Data Models & Schemas](#3-data-models--schemas)  
4. [End-to-End Request Flow](#4-end-to-end-request-flow)  
5. [Caching Strategy – Low-Level Design](#6-caching-strategy--low-level-design)  
6. [Error Handling & Edge Cases](#7-error-handling--edge-cases)  
7. [Evaluation & Benchmarking](#9-evaluation--benchmarking)  
8. [Deployment Details](#10-deployment-details)

# 1. Introduction

## 1.1 Purpose of the Document

This document defines the **Low-Level Design (LLD)** of the **Enterprise Internal HR Knowledge RAG System**.

It describes implementation-level details, including:

- Internal modules and their responsibilities  
- Data structures and interfaces  
- Control flow and request lifecycle  
- Component interactions and dependencies  
- Caching, security, and performance mechanisms  

This LLD is intended to act as a **technical reference** for development, review, and maintenance.

> **Note:** High-level architectural decisions and business context are intentionally excluded.

---

## 1.2 System Overview

The system is an internal **Retrieval-Augmented Generation (RAG)** backend service that allows authenticated users to query enterprise HR documents and receive **context-grounded AI-generated responses**.

**Key characteristics:**

- Implemented as a FastAPI-based REST service  
- Uses JWT authentication with Role-Based Access Control (RBAC)  
- Performs semantic retrieval over internal documents  
- Uses parent–child chunking with reranking  
- Integrates an LLM for answer generation  
- Employs multi-layer caching to reduce latency  
- Designed for containerized deployment  

This section focuses only on what is necessary to understand **module behavior and execution flow**.

---

## 1.3 Design Goals

### Functional Goals

- Retrieve relevant internal knowledge accurately  
- Enforce access control at request and document level  
- Generate context-aware and traceable responses  

### Non-Functional Goals

- Low latency  
- Reliability and fault tolerance  
- Security  
- Maintainability  

> Scalability, observability, and CI/CD are considered only where they directly affect implementation.

---

## 1.4 Target Audience

This document is primarily intended for:

- **Backend Developers** – API behavior, modules, data flow  
- **AI Engineers** – RAG pipeline, embeddings, retrieval, LLM calls  
- **DevOps Engineers** – deployment-related implementation details  
- **Security Engineers** – authentication and authorization logic  

> *(System architects are not the primary audience for LLD.)*

---

## 1.5 Document Scope

### Included

- Module-level design  
- API request/response flow  
- Data structures and schemas  
- Retrieval and generation pipeline  
- Caching logic  
- Security enforcement  
- Performance-related implementation details  

### Excluded

- UI/UX design  
- Business rules and HR policies  
- Organizational workflows  
- Raw document ingestion pipelines  

# Module-Level Design

## 2.1 Application Entry Module

**File:** `app/main.py`

### Purpose
- Starts FastAPI server
- Loads environment variables
- Registers routes

### Responsibilities
- Load `.env` using `load_dotenv()`
- Create FastAPI app
- Register routers:
  - `auth_router`
  - `rag_router`

### Code Flow

load_dotenv()
→ FastAPI()
→ define "/"
→ include auth router
→ include rag router

### Exposed Endpoints
- `/` → health/status
- `/login`
- `/me`
- `/ask`
- `/ask_with_metrics`

---

## 2.2 Configuration Module

**File:** `app/core/config.py`

### Purpose
Central config + secrets management

### Responsibilities
- Load API keys
- Load secrets
- Load thresholds
- Load system parameters

### Data Loaded

#### Auth:
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

#### LLM / AI:
- `OPENAI_API_KEY`
- `GROQ_API_KEY`
- `COHERE_API_KEY`

#### Vector DB:
- `PINECONE_API_KEY`
- `PINECONE_INDEX_NAME`

#### Cache:
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_USERNAME`
- `REDIS_PASSWORD`

#### RAG:
- `TOP_K`
- `PINECONE_SCORE_THRESHOLD`
- `RERANK_SCORE_THRESHOLD`

#### Semantic Cache:
- `SEMANTIC_CACHE_THRESHOLD`
- `SEMANTIC_CACHE_TTL`

### Source of Secrets
Azure App Service Environment Variables  
*(Not .env in production)*

---

## 2.3 Authentication & Authorization Module

**Files:**
- `app/auth/models.py`
- `app/auth/routes.py`
- `app/auth/users.py`
- `app/core/security.py`

### Purpose
This module controls who can access the system and what they are allowed to access.

### User Management
Users are loaded from an internal dataset (`users.xlsx`) into memory at startup.  
Each user contains:
- User ID
- Email
- Hashed password
- Role (`employee`, `hr`, `manager`)
- Status (`active` / `inactive`)

This acts as an internal user directory for authentication.

### Authentication Flow
1. User sends email and password to `/login`
2. System verifies:
   - User exists
   - User is active
   - Password hash matches
3. A JWT token is generated containing:
   - `user_id`
   - `email`
   - `role`
4. Token is returned to the client

### Authorization Flow
For every protected request:
1. JWT token is extracted from the request
2. Token is validated
3. User identity and role are extracted
4. Role information is passed into the RAG pipeline
5. Role is used for:
   - Data filtering
   - Cache isolation
   - Access control

---

## 2.4 RAG API Module

**File:** `app/rag/routes.py`

### Purpose
This module acts as the core execution engine of the system.  
It connects authentication, retrieval, caching, memory, and LLM generation into one pipeline.

### API Endpoints
- `/ask` → returns only the answer
- `/ask_with_metrics` → returns answer + latency + usage + cache info

**Query:**
{
  "question": "str"
}

**Response Format:**
- `/ask` → returns just the `"answer"`
- `/ask_with_metrics` → returns:
  - `answer`
  - `latency`
  - `token usage`
  - `cache info`

## How the RAG Pipeline Works

1. **User request is received**
2. **User identity and role are extracted**
3. **Question embedding is generated**
4. **Semantic cache is checked**
5. **If hit → answer returned directly**
6. **Vector search is performed in Pinecone**
7. **Sparse search (BM25) is applied**
8. **Role-based filtering is enforced**
9. **Results are reranked using Cohere**
10. **Parent documents are reconstructed**
11. **Context is built**
12. **Conversation memory is added**
13. **LLM is invoked**
14. **Answer is generated**
15. **Cache is updated**
16. **Memory is updated**
17. **Response is returned**

---

## 2.5 LLM & Embedding Client Module

**File:** `app/rag/clients.py`

### Purpose
This module manages all external AI service connections.

### Services Handled
- **OpenAI** → embeddings
- **Pinecone** → vector database
- **BM25** → sparse retrieval
- **Cohere** → reranking
- **Groq** → LLM inference

### How It Works
- API keys are loaded from config
- Clients are initialized once
- Shared across the system
- Abstracted away from business logic

### Why This Design
- **Centralized API management**
- **Easy service replacement**
- **Clean separation of infrastructure and logic**
- **Supports multi-provider architecture**

---

## 2.6 Document Storage & Retrieval Module

**File:** `app/rag/parent_store.py`

### Purpose
This module manages parent document reconstruction.

### How Data is Structured
- Child chunks are stored in Pinecone
- Each child chunk contains a `parent_id`
- Parent documents are stored locally
- Parent store maps `parent_id` → full document

### How It Works
1. **Retrieval returns child chunks**
2. **Each chunk references a parent document**
3. **Parent text is fetched using `parent_id`**
4. **Full context is reconstructed using:**
   - Parent text
   - Child chunk text
## 2.7 Caching Module

### A. Conversation Memory Cache

**File:** `app/cache/memory.py`

#### Purpose
To maintain conversation context within a user session.

#### How It Works
Each user session stores:

1. **Recent raw conversation turns:**  
   `chat:{session_id}:turns` stores recent raw conversation turns (user question + AI response).

2. **A summarized long-term memory:**  
   `chat:{session_id}:summary` stores a compressed long-term summary of older conversation history.

#### Flow:
1. Every interaction is stored
2. When conversation grows:
   - Older turns are summarized
   - Summary is stored
   - Raw history is trimmed
3. Memory is injected into the LLM prompt

#### Design Benefits
- **Maintains context**
- **Controls token usage**
- **Prevents memory overflow**
- **Supports multi-turn conversations**
- **Auto-cleanup using TTL**

---

### B. Semantic Cache

**File:** `app/cache/semantic_cache.py`

#### Purpose
To avoid recomputation for similar questions.

**Key Format:** `semantic_cache:{role}:{hash(question)}`

#### Role-Based Cache Separation:
- **employee cache**
- **hr cache**
- **manager cache**

#### How It Works
1. Each question embedding is stored with its answer
2. New queries are compared using cosine similarity
3. If similarity exceeds threshold:
   - Cached answer is returned
   - Retrieval is skipped
   - Reranking is skipped
   - LLM is skipped

#### Role Isolation
Cache is separated by user role, ensuring:
- No cross-role data leakage
- Access control integrity

#### Design Benefits
- **Major latency reduction**
- **Cost reduction**
- **Load reduction**
- **Faster user response**
- **Safe reuse of knowledge**

---

### C. Redis Backend

**File:** `app/cache/redis_client.py`

#### Purpose
Acts as the central caching backend.

#### Behavior
- **If Redis is available** → caching enabled
- **If Redis is unavailable** → system runs without cache

#### Why This Design
- **Fault-tolerant architecture**
- **No single point of failure**
- **Graceful degradation**

---

## 2.8 Data Models Module

**File:** `app/models/query.py`

### Query Model
{
  "question": "str"
}

## 2.9 Evaluation & Latency Analysis Module

**Directories:**
- `eval_scripts/`
- `eval_data/`
- `evaluation/`

### Purpose
This module provides a formal evaluation framework to measure:

- **System performance**
- **Latency**
- **Retrieval quality**
- **RBAC correctness**
- **Answer quality**
- **Cost impact**

It ensures the system is **measurable, testable, and verifiable**, not just functional.

### Evaluation Architecture
The evaluation system is separated into three layers:

#### 1) Test Data Layer (`eval_data/`)
- Stores structured evaluation datasets in `.jsonl` format
- Each file represents a different evaluation dimension:
  - `latency_eval.jsonl` → performance testing
  - `retrieval_eval.jsonl` → retrieval accuracy
  - `rbac_eval.jsonl` → role-based access correctness
  - `generational_eval.jsonl` → answer quality

This separation ensures **controlled, repeatable testing**.

#### 2) Execution Layer (`eval_scripts/`)
These scripts automate testing by calling live APIs:

- `run_latency_eval.py` → Measures response time across pipeline stages
- `run_retrieval_eval.py` → Tests quality of retrieved documents
- `run_rbac_eval.py` → Validates role-based access control
- `run_generation_eval.py` → Evaluates answer quality

**Each script:**
- Sends real API requests
- Captures responses
- Stores structured results
- Produces measurable outputs

This ensures **real-system evaluation**, not simulated testing.

#### 3) Analysis Layer (`evaluation/`)
- Jupyter notebooks process raw evaluation data:
  - Latency breakdown
  - Cost analysis
  - Accuracy metrics
  - Retrieval precision
  - RBAC validation
  - Generation quality
- `metrics_summary.md` provides a consolidated evaluation report

### Latency Measurement Design
Latency is measured at multiple pipeline stages:

1. **Authentication time**
2. **Embedding generation time**
3. **Retrieval time**
4. **Reranking time**
5. **LLM generation time**
6. **Total request time**

This enables **bottleneck identification** and **targeted optimization**.

### Retrieval Evaluation
Retrieval quality is evaluated by:

- **Comparing expected vs retrieved documents**
- **Measuring relevance accuracy**
- **Validating parent–child reconstruction**
- **Testing reranking effectiveness**

This ensures that answers are based on **correct source documents**, not hallucinations.

### RBAC Evaluation
RBAC testing ensures:

- **Employees** only access employee-level data
- **Managers** only access manager-level data
- **HR** only accesses HR-level data
- **No cross-role leakage**
- **Cache isolation correctness**

This validates **security correctness**, not just functionality.

### Generation Quality Evaluation
Answer quality is evaluated using:

- **Consistency checks**
- **Context grounding checks**
- **Relevance checks**
- **Hallucination detection**
- **Role-appropriateness validation**

This ensures the LLM output is:

✅ **Accurate**  
✅ **Grounded**  
✅ **Role-safe**  
✅ **Context-aware**

## 3. Data Models & Schemas

This section defines the actual data structures used in the system. It documents how data is represented, stored, transferred, and processed across different modules.

### 3.1 Query Request Model

**Source:** `app/models/query.py`

**Purpose**

Represents the user input sent to the RAG system.

**Structure**

Query:
{
  "question": "string"
}

**Explanation:**

Used for user authentication. The user provides email and password, which are validated against the internal user database.

**Token Response Model**

TokenResponse:
{
  "access_token": "string",
  "token_type": "bearer",
  "role": "string"
}

**Explanation:**

After successful login:

- **access_token** → JWT token for authentication
- **token_type** → always `bearer`
- **role** → user role (`employee`, `hr`, `manager`)

This token is used for all protected API calls.

### 3.3 API Response Structure

**Source:** `app/rag/routes.py`

**Basic Response (`/ask`)**

{
  "answer": "string"
}

**Explanation:**

Returns only the generated answer when metrics are not requested.

**Extended Response (`/ask_with_metrics`)**

    ```json
    {
      "answer": "string",
      "latency": {
        "total": number,
        "embedding": number,
        "retrieval": number,
        "reranker": number,
        "llm": number
      },
      "usage": {
        "embedding_tokens": number,
        "llm_input_tokens": number,
        "llm_output_tokens": number,
        "reranker_calls": number
      },
      "cache": {
        "semantic_cache_hit": boolean
      }
    }
    ```

**Explanation:**

This structure provides:
- AI-generated answer
- Detailed latency breakdown
- Token usage information
- Cache hit/miss information

This is used for evaluation and performance analysis.

### 3.4 User Data Structure

**Source:** `app/auth/users.py`

**Internal User Object**

```json
{
  "user_id": "number | string",
  "email": "string",
  "hashed_password": "string",
  "role": "string",
  "status": "string"
}
```

**Explanation:**
This structure represents users loaded from users.xlsx and stored in memory.
It is used for authentication, authorization, and RBAC enforcement.

### 3.5.1 Child Chunk Structure (Pinecone Vector Store)

Each vector stored in Pinecone represents a child chunk of a document.

**Structure Example:**

child_chunk =
```json 
{
  "id": "string",
  "child_id": "string",
  "text": "string",
  "parent_id": "string",
  "category": "string",
  "source": "string",
  "employee": "boolean",
  "hr": "boolean",
  "manager": "boolean"
}
```

### 3.5.2 Role-Based Filtering (RBAC at Retrieval Level)


Role-based filtering is applied **directly at Pinecone query time**.


#### Filter Logic (from code)


```python
filter = {
role: {"$eq": True}
}

Where:

- `role ∈ { "employee", "hr", "manager" }`
```
#### Meaning

- If user role = **"hr"** → only chunks with `hr: true` are retrieved  
- If user role = **"employee"** → only chunks with `employee: true` are retrieved  
- If user role = **"manager"** → only chunks with `manager: true` are retrieved

### Explanation

This means:

- Unauthorized chunks are **never retrieved**
- Unauthorized data **never enters the pipeline**
- Unauthorized content is **never cached**
- Unauthorized content is **never passed to the LLM**

This enforces **hard RBAC at the data layer**, not just the API layer.

### 3.5.3 Parent Document Structure (Parent Store)

Parent documents are stored locally and referenced using `parent_id`.

#### Parent Store Structure

```python
parent_store[parent_id] = {
    "id": string,
    "text": string,
    "metadata": {
        "source": string,
        "category": string,
        "employee": boolean,
        "hr": boolean,
        "manager": boolean,
        "parent_id": string
    }
}
```

### 3.5.4 Parent–Child Linking Model

#### Relationship

- **Child chunk** → `parent_id` → **Parent document**

#### Flow

1. Pinecone returns **child chunks**
2. Each chunk contains a `parent_id`
3. System queries `parent_store[parent_id]`
4. Parent text is fetched
5. Context is constructed using:
   - Parent text
   - Child chunk text.
## Where Role Filtering Happens (LLD Explanation)

Role filtering is applied at **three levels** in the system to ensure strict access control and data isolation.

---

### 1) Retrieval Level (Pinecone)

**Filter Configuration:**
```python
filter = { role: { "$eq": True } }
```

### Behavior

- Only authorized chunks are retrieved  
- Unauthorized documents are never returned from the vector store  

---

### 2) Cache Level (Semantic Cache)
```text
semantic_cache:{role}:*
```
➡ Cache is **role-isolated**  
➡ HR cache ≠ Employee cache ≠ Manager cache

#### 3) Pipeline Level

```python
current_user["role"]
```

