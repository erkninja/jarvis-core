01 - Architecture

Overview

JARVIS is composed of small, independent components that each have a single responsibility.

Each component receives information, performs one job, and passes the result to the next component.

This allows the system to evolve without tightly coupling one part of the application to another.

⸻

High-Level Flow

User
↓
Voice or Text Client
↓
Speech Recognition (voice only)
↓
Cleanup Preprocessor
↓
Fast Response Handler
↓
Request Parser
↓
JARVIS Core
↓
Plugin
↓
Response Generator
↓
Voice or Text Client
↓
User

⸻

Components

Voice or Text Client

The client is how the user interacts with JARVIS.

Examples include:

* ESP32 voice satellite
* Mobile application
* Web interface
* Terminal
* Future integrations

The client is responsible only for communicating with the user.

It should not contain business logic.

⸻

Speech Recognition

Speech Recognition converts spoken audio into text.

It does not determine what the user means.

Its only responsibility is producing an accurate transcript.

⸻

Cleanup Preprocessor

The Cleanup Preprocessor prepares a user’s utterance for further processing.

Its purpose is to perform simple, deterministic transformations that remove unnecessary information while preserving the user’s intent.

Examples include:

* Removing wake words.
* Removing the assistant’s name when used only to address JARVIS.
* Normalizing whitespace.
* Performing other predefined text cleanup operations.

The Cleanup Preprocessor does not understand language, infer intent, classify requests, or modify the meaning of the user’s utterance.

Its only responsibility is to produce a clean representation of what the user said before it is passed to the next stage of the processing pipeline.

⸻

Fast Response Handler

The Fast Response Handler provides immediate responses for simple, deterministic interactions without invoking the Request Parser or an AI model.
Its purpose is to make interactions feel natural by avoiding unnecessary processing for common conversational exchanges.

Examples include:

* Wake acknowledgement
* Greetings
* Expressions of thanks
* Session cancellation
* Other predefined responses that do not require interpretation

The Fast Response Handler must never consume an utterance that contains an executable request.

For example:

* “Hi Jarvis.” → Respond immediately.
* “Thanks.” → Respond immediately.
* “Never mind.” → Cancel the current request or session.
* “Hi Jarvis, turn on the lights.” → Pass the remaining request to the Request Parser.

The Fast Response Handler should remain deterministic and lightweight. It is not intended to understand natural language or infer user intent.
It only handles exact/near-exact allowlisted phrases.
⸻

Request Parser

The Request Parser analyzes what the user said and converts it into a structured request that JARVIS can understand.

It understands language.

It does not execute requests.

It does not know about Home Assistant, TrueNAS, or any other implementation details.

The parser extracts words. Plugins assign meaning.
⸻

JARVIS Core

JARVIS Core is the heart of the system.

Its responsibilities include:

* Maintaining conversation context
* Routing requests
* Coordinating plugins
* Recording execution history
* Managing the overall flow of the application

JARVIS Core understands the architecture of the system but does not understand the implementation details of any specific plugin.

⸻

Plugins

Plugins provide the actual capabilities of JARVIS.

Each plugin owns a single domain.

Examples include:

* Home Assistant
* Calendar
* TrueNAS
* Email
* Media

A plugin is responsible for understanding and interacting with the system it represents.

For example, the Home Assistant plugin knows about lights, locks, thermostats, and other smart home devices.

The Calendar plugin knows about calendars and events.

JARVIS Core never attempts to replace this knowledge.

⸻

Response Generator

After a request has been completed, the Response Generator determines what should be communicated back to the user.

Examples include:

* “Done.”
* “The office lights are now on.”
* “You have three meetings today.”

This component controls how JARVIS communicates, but it does not influence how requests are executed.

⸻

Design Principles

Single Responsibility

Every component should perform one job well.

⸻

Separation of Concerns

Language understanding, request routing, execution, and communication are separate responsibilities.

⸻

Plugin Ownership

Each plugin is the authoritative source for its own domain.

⸻

Implementation Independence

The Request Parser should not know about plugins.

Plugins should not know about the internals of JARVIS Core.

Each component communicates only through well-defined interfaces.

⸻

Extensibility

JARVIS Core maintains a registry of the capabilities available to the system.

Plugins register the objects and actions they support during initialization.

When a request is received, JARVIS Core uses this registry to determine which plugin is responsible for handling the request.

Adding new capabilities should normally involve creating or extending a plugin and registering its capabilities with JARVIS Core, rather than modifying the routing logic itself.

This allows the system to grow while keeping responsibilities clearly separated between the core and individual plugins.

⸻

Request Lifecycle

1. The user makes a request.
2. The request is converted into text if necessary.
3. The Request Parser determines what the user is asking.
4. JARVIS Core determines which plugin owns the requested capability.
5. The selected plugin performs the requested work.
6. The result is returned to JARVIS Core.
7. The Response Generator creates a natural response.
8. The response is returned to the user.

⸻

Future Expansion

The architecture is designed so additional capabilities can be added without redesigning the system.

Examples include:

* Voice identification
* Vision processing
* Learning and personalization
* Mobile applications
* Web dashboards
* Additional plugins
* Additional client types