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


2. Module-Level Design
2.1 Application Entry Module

File: app/main.py

Purpose

Starts FastAPI server

Loads environment variables

Registers routes

Responsibilities

Load .env using load_dotenv()

Create FastAPI application

Register routers:

auth_router

rag_router
