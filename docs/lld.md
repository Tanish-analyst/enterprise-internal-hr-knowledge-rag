# 📘 Low-Level Design (LLD)
## Enterprise Internal HR Knowledge RAG System

---

## 📑 Table of Contents

1. [Introduction](#1-introduction)  
2. [Module-Level Design](#2-Module-Level-Design)  
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
- 
## 2. Module-Level Design
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

# 3-data-models--schemas
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

➡ **Role controls:**


- Retrieval filter
- Cache lookup
- Cache storage
- Context building
- Answer reuse

# 3.7 Conversation Memory Data Structures

**Source:** `app/cache/memory.py`

## Raw Turn Structure

```json
{
  "user": "string",
  "assistant": "string",
  "ts": "number"
}
```

**Storage Key:**

* `chat:{session_id}:turns`

**Explanation:**

* Stores recent conversation turns for session-level memory.

---

## Summary Structure

```json
{
  "summary": "string"
}
```

**Storage Key:**

* `chat:{session_id}:summary`

**Explanation:**

* Stores summarized long-term memory of the conversation for context preservation.

---

# 3.8 Redis Connection Structure

**Source:** `app/cache/redis_client.py`

## Redis Client Object

```python
redis_client = Redis(
  host,
  port,
  username,
  password
)
```

**Explanation:**
Central Redis connection object used by:

* Semantic cache
* Conversation memory
* TTL management
* Session cleanup

---

# 3.9 Evaluation Data Structures

**Source:** `eval_data/*.jsonl`

## Common JSONL Structure

Each line represents one evaluation case:

```json
{
  "question": "string",
  "expected": "string",
  "role": "string",
  "metadata": "object"
}
```

**Explanation:**
Evaluation datasets store:

* Test questions
* Expected outputs
* Role context
* Evaluation metadata

Used by evaluation scripts and notebooks.

---

# 4. End-to-End Request Flow

This section defines the exact execution flow of a request through the system, from API entry to response return.

---

## 4.1 Request Entry and Validation

**Endpoints:**

* `POST /ask`
* `POST /ask_with_metrics`

### Flow

* HTTP request received
* FastAPI route handler
* Payload parsed into Query model
* Schema validation (Pydantic)
* Invalid request → `422`

---

## 4.2 Authentication and RBAC Check

**Header:** `Authorization: Bearer <JWT>`

### Flow

* Extract JWT token
* Verify token signature
* Decode token
* Extract:

  * user_id
  * email
  * role
* If invalid → `401`
* If inactive → `403`

---

## 4.3 Session Context Resolution

```text
session_id = current_user["user_id"]
role       = current_user["role"]
question   = payload.question
```

---

## 4.4 Embedding Generation

**Service:** OpenAI Embedding API

### Flow

* question → embedding model
* query_embedding vector
* embedding_tokens
* embedding_latency

---

## 4.5 Semantic Cache Lookup (Cache Hit Flow)

**Function:** `semantic_cache_lookup(role, query_embedding)`

### Flow

* Redis scan by role
* Cosine similarity calculation
* Best match selection
* Similarity threshold check

### If HIT

* Answer fetched
* Skip retrieval
* Skip reranking
* Skip parent lookup
* Skip LLM
* Build response
* Return response

---

## 4.6 Semantic Cache Miss Flow

* `semantic_cache_lookup → MISS`

---

## 4.7 Vector Retrieval

**Service:** Pinecone

### Query Structure

* `vector = query_embedding`
* `top_k = TOP_K`
* `filter = { role: { "$eq": true } }`
* `sparse_vector = BM25 (if available)`

### Flow

* Vector search
* Hybrid retrieval (dense + sparse)
* Role-based filtering
* Child chunks returned

---

## 4.8 Empty Retrieval Handling

**Condition:** `results.matches == empty`

### Flow

* Return "No data found"
* End request

---

## 4.9 Reranking

**Service:** Cohere reranker

### Flow

* Retrieved chunks
* Rerank model
* Relevance scoring
* Threshold filtering
* Top ranked chunks selected

---

## 4.10 Parent–Child Reconstruction

**Mapping:** `child_chunk.parent_id → parent_store[parent_id]`

### Flow

* Fetch parent document
* Combine parent text + child text
* Build context

---

## 4.11 Memory Context Injection

**Function:** `build_memory_context(session_id)`

### Flow

* Fetch summary
* Fetch recent turns
* Construct message list
* Attach to prompt

---

## 4.12 LLM Execution

**Call:** `LLM.invoke()`

### Input Structure

* memory_context
* system_prompt
* context
* question

### Flow

* LLM call
* Response generated
* Token usage recorded
* Latency recorded

---

## 4.13 Semantic Cache Storage

**Function:** `store_semantic_cache(role, question, embedding, answer)`

### Flow

* Create role-based cache key
* Store embedding
* Store answer
* Store timestamp

---

## 4.14 Memory Update

**Functions:**

* `store_turn(session_id, turn)`
* `maybe_summarize(session_id, llm)`

### Flow

* Store raw turn
* Check summary trigger
* Summarize old turns
* Update summary
* Trim old turns

---

## 4.15 Response Construction

### Without Metrics

```json
{
  "answer": "string"
}
```

### With Metrics

```json
{
  "answer": "string",
  "latency": { },
  "usage": { },
  "cache": { }
}
```

---

## 4.16 Response Return

* FastAPI → HTTP response → Client

---

# 6. Caching Strategy – Low-Level Design

This section defines the caching architecture, data flow, and behavior of caching mechanisms used in the system.

---

## 6.1 Cache Architecture Overview

The caching layer consists of:

* Conversation Memory Cache
* Semantic Cache
* Redis Backend Layer

---

## 6.2 Conversation Memory Cache

**File:** `app/cache/memory.py`

### Purpose

* Maintain short-term and long-term conversational context

### Data Stored

* Raw Turns → `chat:{session_id}:turns`
* Summary   → `chat:{session_id}:summary`

### Storage Model

* Turns → Redis list
* Summary → Redis string

### Update Flow

* User query + AI answer
* `store_turn(session_id, turn)`
* Turn appended to Redis list

### Summarization Flow

* If turns > `SUMMARY_TRIGGER`
* Summarize using LLM
* Update summary
* Trim old turns

### TTL Behavior

* `TTL_SECONDS = 300`
* Inactive session → auto-deleted

### Design Purpose

* Conversational continuity
* Token control
* Memory growth control
* Multi-turn support
* Session context
* Automatic cleanup

---

## 6.3 Semantic Cache

**File:** `app/cache/semantic_cache.py`

### Purpose

* Avoid recomputation for semantically similar queries

### Cache Key

* `semantic_cache:{role}:{hash(question)}`

### Data Stored

```json
{
  "role": "string",
  "question": "string",
  "embedding": "vector",
  "answer": "string",
  "ts": "number"
}
```

### Lookup Flow

* Query embedding
* Scan keys by role
* Cosine similarity
* Best match
* Threshold check

### Cache Hit Behavior

* Return cached answer
* Skip retrieval
* Skip reranking
* Skip parent lookup
* Skip LLM

### Cache Miss Behavior

* Continue RAG pipeline
* Generate answer
* Store in semantic cache

### Role Isolation

* `semantic_cache:employee:*`
* `semantic_cache:hr:*`
* `semantic_cache:manager:*`

### Design Purpose

* Latency reduction
* Cost reduction
* Load reduction
* Fast responses
* RBAC-safe reuse

---

## 6.4 Redis Backend Layer

**File:** `app/cache/redis_client.py`

### Purpose

* Central cache storage engine

### Behavior

* Redis connected → caching enabled
* Redis unavailable → caching disabled

### Failure Handling

* Redis failure → system continues without cache

### Design Purpose

* Fault tolerance
* Graceful degradation
* No single point of failure
* System availability

---

## 6.5 Cache Interaction Flow

```
Request → Semantic Cache
        → (hit) → return answer
        → (miss) → RAG pipeline
                      → generate answer
                      → store semantic cache
                      → update memory cache
```

---

## 6.6 Cache Consistency Model

* Conversation Memory → session-scoped
* Semantic Cache → role-scoped

---

## 6.7 Cache Scope

* Conversation Memory → per session
* Semantic Cache → per role

---

# 7. Error Handling & Edge Cases

This section defines system failure handling, exceptions, and abnormal conditions.

---

## 7.1 Authentication Failures

### Invalid Credentials

* Email not found
* Password mismatch

**Behavior:**

* HTTP 401
* Request terminated

### Inactive User

* status != "active"

**Behavior:**

* HTTP 403
* Access denied

### Invalid Token

* Invalid JWT
* Expired JWT
* Corrupt token

**Behavior:**

* HTTP 401
* Request terminated

---

## 7.2 Authorization Failures (RBAC)

**Behavior:**

* Role filter applied
* Unauthorized chunks not retrieved
* No data exposure

If no authorized data:

* Empty retrieval
* Return "No data found"

---

## 7.3 Configuration Failures

### Missing Clients

* openai_client == None
* pinecone_index == None
* bm25 == None

**Behavior:**

* HTTP 500
* Server not configured

---

## 7.4 Cache Failures

### Redis Unavailable

**Behavior:**

* semantic cache disabled
* memory cache disabled
* system continues

### Semantic Cache Errors

**Behavior:**

* lookup failure → ignore cache
* store failure → ignore cache
* continue pipeline

---

## 7.5 Retrieval Failures

### Empty Retrieval

**Behavior:**

* Return "No data found"
* Skip reranking
* Skip LLM

### Sparse Encoder Failure (BM25)

**Behavior:**

* Sparse disabled
* Dense retrieval only

---

## 7.6 Reranker Failures

### Cohere API Failure

**Behavior:**

* Fallback to top-k chunks
* Continue pipeline

---

## 7.7 Parent Store Failures

### Missing Parent Document

**Behavior:**

* parent_text = ""
* Use child chunk only
* Continue context

---

## 7.8 LLM Failures

### LLM API Error

**Behavior:**

* HTTP 500
* Request failed

---

## 7.9 Timeout Handling

### External Service Timeout

**Behavior:**

* Exception
* Request failed
* Error response

---

## 7.10 Partial Pipeline Failures

### Non-Critical Failures

* Semantic cache failure
* Memory store failure
* Reranker failure

**Behavior:**

* Component bypassed
* Pipeline continues
* System functional

---

## 7.11 Graceful Degradation Model

* Redis down → caching disabled
* BM25 fails → dense only
* Reranker fails → unranked retrieval
* Parent missing → child-only context

---

## 7.12 Failure Isolation Model

* Cache failure ≠ pipeline failure
* Memory failure ≠ pipeline failure
* Reranker failure ≠ pipeline failure

Failures are isolated to individual components.

# 9. Evaluation & Benchmarking

This section defines how the system is tested, measured, and validated using automated evaluation pipelines and structured datasets.

The evaluation framework ensures the system is measurable, verifiable, and auditable — not just functional.

---

## 9.1 Evaluation Architecture

Evaluation is implemented as a separate subsystem with three layers:

* **Test Data Layer** → `eval_data/`
* **Execution Layer** → `eval_scripts/`
* **Analysis Layer** → `evaluation/`

---

## 9.2 Test Data Layer

**Directory:** `eval_data/`

### Files

* `generational_eval.jsonl`
* `latency_eval.jsonl`
* `rbac_eval.jsonl`
* `retrieval_eval.jsonl`

### Purpose

* `generational_eval.jsonl` → answer quality evaluation
* `latency_eval.jsonl` → performance evaluation
* `rbac_eval.jsonl` → role access validation
* `retrieval_eval.jsonl` → retrieval accuracy evaluation

---

## 9.3 Execution Layer

**Directory:** `eval_scripts/`

### Scripts

* `run_generation_eval.py`
* `run_latency_eval.py`
* `run_rbac_eval.py`
* `run_retrieval_eval.py`

### Execution Model

```text
script → API calls → collect responses → store results
```

Each script:

* Sends real requests to the FastAPI backend
* Uses real authentication
* Uses real RBAC
* Uses real retrieval
* Uses real LLM
* Uses real cache behavior

---

## 9.4 Latency Evaluation

### Files

* `latency_eval.jsonl`
* `run_latency_eval.py`
* `latency_cost_eval.ipynb`

### Metrics Collected

* Total latency
* Embedding latency
* Retrieval latency
* Reranker latency
* LLM latency

### Purpose

* Identify bottlenecks
* Measure pipeline performance
* Compare cache hit vs cache miss
* Measure optimization impact

---

## 9.5 Retrieval Evaluation

### Files

* `retrieval_eval.jsonl`
* `run_retrieval_eval.py`
* `retrieval_eval.ipynb`

### Metrics

* Retrieval accuracy
* Relevance quality
* Parent–child correctness
* Reranking effectiveness

---

## 9.6 RBAC Evaluation

### Files

* `rbac_eval.jsonl`
* `run_rbac_eval.py`
* `rbac_eval.ipynb`

### Validation Scope

* Role-based filtering correctness
* Unauthorized data access prevention
* Cross-role leakage detection
* Cache role isolation validation

---

## 9.7 Generation Quality Evaluation

### Files

* `generational_eval.jsonl`
* `run_generation_eval.py`
* `generation_eval.ipynb`

### Evaluation Scope

* Answer relevance
* Context grounding
* Hallucination detection
* Role-appropriate answers
* Consistency

---

## 9.8 Analysis Layer

**Directory:** `evaluation/`

### Files

* `generation_eval.ipynb`
* `latency_cost_eval.ipynb`
* `rbac_eval.ipynb`
* `retrieval_eval.ipynb`
* `metrics_summary.md`

### Role

* Metrics aggregation
* Performance analysis
* Visualization
* Trend analysis
* Quality scoring
* Benchmark reporting

---

## 9.9 Metrics Consolidation

**File:** `metrics_summary.md`

### Purpose

* Central evaluation report
* System performance summary
* Quality metrics summary
* Security validation summary
* Retrieval performance summary

---

## 9.10 Benchmarking Model

* Offline datasets
* Automated scripts
* Live system execution
* Real API calls
* Real latency measurement
* Real cache behavior
* Real RBAC enforcement

---

## 9.11 Evaluation Characteristics

* Repeatable
* Automated
* Measurable
* Verifiable
* Auditable
* Regression-test capable


# 10. Deployment Details

This section defines how the system is built, configured, deployed, and executed in production environments.

It describes the deployment model, environment handling, secret management, runtime behavior, and CI/CD integration.

---

## 10.1 Docker Deployment

**Source:** Dockerfile

### Deployment Model

* Application packaged as a container image

### Build Process

* Source code
* Docker build
* Dependency installation
* FastAPI app setup
* Runtime container image

### Purpose

* Environment consistency
* Reproducible builds
* Deployment portability
* Platform independence

---

## 10.2 Azure Deployment

### Platform

* Azure App Service (Container-based deployment)

### Deployment Model

* Docker image → Azure App Service

### Runtime Behavior

* Container runs FastAPI service
* External services connected at runtime
* Stateless API execution

---

## 10.3 Environment Handling

### Configuration Source

* Azure App Service Environment Variables

### Behavior

* No `.env` dependency in production
* No hardcoded secrets
* All configs injected at runtime

---

## 10.4 Secret Injection

### Secrets Managed

* OPENAI_API_KEY
* GROQ_API_KEY
* COHERE_API_KEY
* PINECONE_API_KEY
* REDIS_HOST
* REDIS_PORT
* REDIS_USERNAME
* REDIS_PASSWORD
* SECRET_KEY

### Injection Model

* Azure → Environment Variables → `app/core/config.py`

---

## 10.5 Runtime Model

### Execution Model

* Single container instance
* FastAPI synchronous execution
* External API dependencies
* Network-bound pipeline

### Runtime Characteristics

* Stateless API layer
* State stored in Redis
* Session memory TTL-based
* External vector DB
* External LLM services

---

## 10.6 CI/CD Workflow Overview

**Source:** `.github/workflows/docker-build.yml`

### Pipeline Flow

* GitHub push
* GitHub Actions trigger
* Docker build
* Build validation
* Image generation

### Purpose

* Continuous integration
* Build verification
* Deployment readiness
* Artifact generation

---

## 10.7 Deployment Characteristics

* Containerized service
* Cloud-native deployment
* Externalized configuration
* Secure secret management
* Stateless execution
* Scalable deployment model
