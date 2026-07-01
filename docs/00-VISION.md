# 00 - Vision

# JARVIS Core

## Mission

JARVIS (Just A Rather Very Intelligent Residential System) is a modular home operating system that provides a natural language interface to the systems, devices, and services within a user's environment.

JARVIS is not a chatbot.

JARVIS is an orchestration platform that understands user intent, maintains conversational context, and coordinates specialized plugins to perform actions.

---

# Objectives

JARVIS should allow users to interact naturally with their home, computers, services, and personal information without needing to remember specific commands or implementation details.

The user should be able to communicate with JARVIS as they would another person.

Examples include:

* "Turn on the lights."
* "What's on my calendar today?"
* "Restart Plex."
* "How much storage is left on the NAS?"
* "Lock the front door at 10 PM."

---

# Design Philosophy

## Understand language, not commands.

Users should never need to memorize syntax.

JARVIS should understand natural language and translate it into structured requests.

---

## Separate understanding from execution.

JARVIS is composed of independent components with clearly defined responsibilities.

* The Request Parser understands language.
* JARVIS Core manages context, routing, and orchestration.
* Plugins understand their own domains.
* Execution Result Handling communicates the outcome of completed actions.

Each component should perform one responsibility well.

---

## Keep implementation details hidden.

The Request Parser should never know:

* Home Assistant
* TrueNAS
* Google Calendar
* Gmail
* Plex
* Spotify
* APIs
* Entity IDs

It only understands language.

JARVIS Core understands the architecture.

Plugins understand their own domains.

---

## Plugins own their domain.

Each plugin is the authoritative source for the resources it manages.

Examples include:

### Home Assistant Plugin

* Lights
* Locks
* Climate
* Sensors
* Media Players

### Calendar Plugin

* Calendars
* Events
* Tasks

### TrueNAS Plugin

* Pools
* Datasets
* Services
* Storage

JARVIS Core never attempts to replace this knowledge.

---

## Context belongs to JARVIS.

Conversation state is maintained by JARVIS Core.

The Request Parser does not remember previous requests.

Plugins do not remember previous requests.

JARVIS maintains conversational context and provides it when needed.

---

## Prefer deterministic knowledge.

If JARVIS can determine something directly, it should not ask an AI model to infer it.

Examples include:

* Current time
* Current date
* Current room
* Current user
* Device state
* Active session

Artificial intelligence should be used to understand language, not to replace information already available to the system.

---

## Everything should be traceable.

Every interaction should produce an execution trace.

A trace should include:

* Original user utterance
* Semantic Request
* Routing decision
* Plugin execution
* Execution result

The trace exists to support debugging, testing, analytics, and future improvements.

---

# Scope

JARVIS is responsible for:

* Understanding natural language
* Maintaining conversational context
* Routing requests
* Coordinating plugins
* Executing actions
* Managing user interactions

JARVIS is not responsible for:

* Home automation
* Calendar management
* Email services
* File storage
* Speech recognition
* Large language model implementation

These responsibilities belong to external systems that JARVIS integrates with.

---

# Long-Term Vision

JARVIS is designed to become a semantic operating system capable of interacting with any service that exposes a compatible plugin.

Voice is only one interface.

The same Semantic Request should be executable regardless of whether it originates from:

* Voice
* Mobile
* Web
* Terminal
* API
* Automation

Every client communicates with the same JARVIS Core.

By separating language understanding from execution, JARVIS can evolve independently of specific AI models, smart home platforms, or user interfaces.

The long-term goal is to create a system that feels less like issuing commands to software and more like interacting with a knowledgeable assistant that understands both natural language and the user's environment.
