# JARVIS Core

**JARVIS (Just A Rather Very Intelligent Residential System)** is a modular home operating system that provides a natural language interface to smart home devices, personal services, and external systems.

JARVIS is designed to understand what a user is asking, coordinate the appropriate systems, and provide a natural conversational experience without exposing implementation details.

---

# Vision

JARVIS is **not** a chatbot.

JARVIS is an orchestration platform that understands user intent, maintains conversational context, and coordinates specialized plugins to perform actions.

The goal is to allow users to interact naturally with their environment rather than memorizing commands or automation names.

---

# Design Goals

* Natural language interaction
* Modular plugin architecture
* Clear separation of responsibilities
* Extensible design
* Vendor-independent architecture
* Fast, responsive conversations

---

# Architecture

At a high level, JARVIS follows this flow:

```text
User
    │
Voice / Text Client
    │
Fast Response Handler
    │
Request Parser
    │
Semantic Request
    │
JARVIS Core
    │
Capability Registry
    │
Plugin
    │
Execution Result Handler
    │
User
```

The Request Parser understands language.

JARVIS Core understands the system architecture.

Plugins understand their own domains.

---

# Project Structure

```text
jarvis-core/
├── docs/
├── src/
├── tests/
└── examples/
```

## Documentation

| Document                 | Purpose                                 |
| ------------------------ | --------------------------------------- |
| `00-VISION.md`           | Project goals and guiding philosophy    |
| `01-ARCHITECTURE.md`     | High-level system architecture          |
| `02-SEMANTIC_REQUEST.md` | Semantic Request protocol specification |

---

# Current Status

The project is currently in the architecture and protocol design phase.

The focus is on defining stable interfaces before implementation begins.

---

# Guiding Principles

* The parser extracts language.
* JARVIS Core owns routing and orchestration.
* Plugins own domain knowledge.
* Deterministic information should not come from AI.
* Unknown values are represented as `null`.
* Complexity should be introduced only when it provides measurable value.

---

# Roadmap

## Phase 1

* Finalize architecture
* Finalize Semantic Request protocol
* Define Plugin API

## Phase 2

* Implement JARVIS Core
* Implement Capability Registry
* Implement plugin framework

## Phase 3

* Home Assistant plugin
* TrueNAS plugin
* Calendar plugin

## Phase 4

* Voice integration
* ESP32 clients
* Local LLM integration

---

# Project Philosophy

JARVIS is built around one central idea:

> **Understand language once. Execute anywhere.**

The Request Parser converts natural language into a structured Semantic Request.

From that point forward, the rest of the system operates on a well-defined protocol, allowing new plugins, clients, and AI models to be added without redesigning the core architecture.
