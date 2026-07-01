## Purpose

This roadmap defines the major milestones for JARVIS Core.

The roadmap is intended to guide development while allowing individual tasks and priorities to evolve over time.

---

# Phase 0 - Foundation ✅

## Goal

Establish the project foundation.

### Deliverables

* Git repository
* Development environment
* Project documentation
* Vision
* Architecture
* Semantic Request specification

---

# Phase 1 - Core Framework

## Goal

Build the core architecture without external integrations.

### Deliverables

* JARVIS Core
* Capability Registry
* Plugin framework
* Context Engine
* Execution pipeline
* Logging framework

### Success Criteria

A manually created Semantic Request can be routed to the correct plugin.

---

# Phase 2 - Home Assistant Integration

## Goal

Allow JARVIS to interact with Home Assistant.

### Deliverables

* Home Assistant plugin
* Capability registration
* Entity resolution
* Action execution

### Success Criteria

JARVIS can successfully control Home Assistant devices using Semantic Requests.

---

# Phase 3 - Request Parser

## Goal

Convert natural language into Semantic Requests.

### Deliverables

* Request Parser prompt
* Semantic Request validation
* Immediate acknowledgements
* Partial Request handling
* Conversation handling

### Success Criteria

Natural language is converted into valid Semantic Requests.

---

# Phase 4 - Voice Interface

## Goal

Enable natural voice interaction.

### Deliverables

* ESP32 voice satellite
* Speech Recognition
* Wake word detection
* Audio streaming
* Text-to-speech

### Success Criteria

A user can control JARVIS entirely through voice.

---

# Phase 5 - Core Plugins

## Goal

Expand JARVIS beyond home automation.

### Initial Plugins

* Calendar
* TrueNAS
* Media
* Weather
* To-Do Lists

### Success Criteria

JARVIS can interact with multiple independent systems through a common architecture.

---

# Phase 6 - Context and Conversation

## Goal

Support natural, multi-turn conversations.

### Deliverables

* Focus object tracking
* Session management
* Context enrichment
* Pronoun resolution
* Conversation continuity

### Success Criteria

Users can naturally refer to previous requests without repeating themselves.

---

# Phase 7 - Personalization

## Goal

Adapt JARVIS to individual users.

### Deliverables

* Voice identification
* User preferences
* Personalized responses
* User-specific defaults

---

# Phase 8 - Learning

## Goal

Allow JARVIS to improve through confirmed user interactions.

### Deliverables

* Alias suggestions
* Learned preferences
* Configuration recommendations
* Usage analytics

Learning should occur only through explicit user confirmation.

---

# Guiding Principles

Development should always prioritize:

1. A working system over a perfect system.
2. Simplicity over unnecessary complexity.
3. Stable interfaces over rapid implementation.
4. Clear responsibilities between components.
5. Incremental progress through small, testable milestones.

New features should be introduced only after there is a demonstrated need for them.

The architecture should remain simple until additional complexity provides measurable value.
