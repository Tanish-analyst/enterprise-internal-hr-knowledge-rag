# SentinelRAG
**Enterprise-Grade Secure Knowledge Intelligence Platform**

## Short Description
A production-grade, secure, role-based Retrieval-Augmented Generation (RAG) platform for internal enterprise knowledge systems. Features include RBAC enforcement, semantic caching, parent–child document retrieval, evaluation pipelines, and cloud-native deployment on Azure.

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

## Key Capabilities

### Secure Internal Knowledge Access
Provides controlled, authenticated access to internal organizational documents through a protected API layer.

### Role-Based Access Control (RBAC)
Enforces strict role-level access (employee, manager, HR) at the data, retrieval, cache, and response layers to prevent unauthorized information exposure.

### Semantic Knowledge Retrieval
Uses embedding-based retrieval to understand user intent and meaning, delivering accurate and relevant results beyond keyword search.

### Hybrid Retrieval Architecture
Combines dense vector search with sparse retrieval for improved recall and precision in document matching.

### Hierarchical Document Structure
Implements parent–child document modeling to preserve document structure and improve contextual coherence in answers.

### Context-Aware Conversational Memory
Supports multi-turn interactions using session memory and summarization for natural conversational access to internal knowledge.

### Role-Isolated Semantic Caching
Accelerates repeated queries through role-scoped semantic caching while maintaining strict data isolation between user roles.

### Enterprise-Grade Security Model
Integrates JWT authentication, RBAC enforcement, role-based filtering, and secure secret handling for production environments.

### Performance-Optimized Pipeline
Uses multi-layer caching, retrieval optimization, and threshold-based reranking to reduce latency and resource consumption.

### Evaluation & Benchmarking Framework
Includes built-in pipelines for latency measurement, retrieval evaluation, RBAC validation, and generation quality assessment.

### Cloud-Native Deployment
Designed for containerized deployment with cloud-native configuration and secure secret injection.

### Production-Ready Architecture
Built with modular components, fault tolerance, graceful degradation, and enterprise deployment practices.

# System Architecture (High-Level)

The system is designed as a secure, layered enterprise platform for internal knowledge access and intelligence.

At a high level, the architecture consists of the following logical layers:

## Client Layer
Internal users and applications interact with the system through a secure API interface.

## Secure API Layer
A protected FastAPI backend handles all incoming requests, authentication, and request validation.

## Identity & Access Layer
JWT-based authentication and role-based access control ensure that users can only access authorized knowledge.

## Knowledge Retrieval Layer
Internal documents are accessed through semantic and hybrid retrieval mechanisms, enabling intelligent knowledge discovery.

## Knowledge Structuring Layer
Parent–child document modeling preserves document hierarchy and ensures coherent context construction.

## AI Intelligence Layer
Retrieved knowledge is processed by AI models to generate grounded, context-aware responses.

## Caching & Memory Layer
Multi-layer caching and session memory optimize performance and enable conversational interaction.

## Infrastructure Layer
The system runs as a cloud-native, containerized service with secure configuration and secret management.

![Architecture Diagram](./docs/HLD/diagrams/architecture_overview.png) 

# Security Model

**Security is a core design principle of the system, not an afterthought.**

The platform is built to ensure that internal organizational knowledge is accessed only by authorized users, under strictly controlled conditions.

---

## Authentication
- **JWT-based Authentication**: The system uses JWT-based authentication for all protected API endpoints.
- **Organizational Credentials**: Users authenticate using valid organizational credentials.
- **Bearer Token Requirement**: Every request to the system requires a valid bearer token.

## Authorization (Role-Based Access Control)
- **RBAC Enforcement**: The system enforces role-based access control (RBAC) across all layers.
- **User Role Definitions**: User roles (employee, manager, HR) define access permissions.
- **Data-Level Control**: Access control is enforced at the data level, not just at the API level.

## Data-Level Role Isolation
- **Role-Access Tagging**: Internal documents are tagged with role-access flags.
- **Role-Based Filtering**: Retrieval operations filter knowledge based on user role.
- **Unauthorized Content Prevention**: Unauthorized documents are never retrieved, processed, cached, or sent to AI models.

## Secure Knowledge Access
- **Authorized Content Only**: Only authorized internal knowledge is used for answer generation.
- **Grounded Responses**: AI responses are grounded strictly in permitted internal content.
- **No External Sources**: No external knowledge sources are used.

## Secure Configuration Management
- **No In-Code Secrets**: Secrets and API keys are never stored in code.
- **Secure Injection**: All credentials are injected through secure environment variables.
- **Cloud-Native Management**: Cloud-native secret management is used in production environments.

## Cache Security
- **Role-Isolated Semantic Cache**: Semantic cache is role-isolated, preventing cross-role data leakage.
- **Session-Scoped Memory**: Session memory is scoped per user session.
- **Consistent Access Control**: Cached data respects the same access control rules as live retrieval.

## Infrastructure Security
- **Containerized Deployment**: Containerized deployment ensures environment isolation.
- **Cloud-Managed Security**: Cloud-managed services handle secure networking and runtime protection.
- **Restricted External Access**: External service access is restricted to required APIs only.

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

