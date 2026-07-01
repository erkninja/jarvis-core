# 01 - Architecture

## Overview

JARVIS is composed of small, independent components that each have a single responsibility.

Each component receives information, performs one task, and passes the result to the next component.

This separation allows the system to evolve without tightly coupling one part of the application to another.

---

# High-Level Flow

```text
                     User
                       │
             Voice or Text Client
                       │
        Speech Recognition (voice only)
                       │
          Cleanup Preprocessor
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
             Voice or Text Client
                       │
                     User
```

---

# Components

## Voice or Text Client

The client is how the user interacts with JARVIS.

Examples include:

* ESP32 voice satellite
* Mobile application
* Web interface
* Terminal
* Future integrations

The client is responsible only for communicating with the user.

It should not contain business logic.

---

## Speech Recognition

Speech Recognition converts spoken audio into text.

Its only responsibility is producing an accurate transcript.

It does not determine what the user means.

---

## Cleanup Preprocessor

The Cleanup Preprocessor prepares a user's utterance for further processing.

Its purpose is to perform simple, deterministic transformations that remove unnecessary information while preserving the user's intent.

Examples include:

* Removing wake words.
* Removing the assistant's name when used only to address JARVIS.
* Normalizing whitespace.
* Performing other predefined text cleanup operations.

The Cleanup Preprocessor does not understand language, infer intent, classify requests, or modify the meaning of the user's utterance.

Its only responsibility is to produce a clean representation of what the user said before it is passed to the next stage of the processing pipeline.

---

## Fast Response Handler

The Fast Response Handler provides immediate responses for simple, deterministic interactions without invoking the Request Parser or an AI model.

Examples include:

* Greetings
* Wake acknowledgements
* Expressions of thanks
* Session cancellation
* Other predefined responses

The Fast Response Handler only handles explicitly configured phrases.

If the utterance contains anything beyond a recognized deterministic interaction, it is forwarded to the Request Parser.

---

## Request Parser

The Request Parser analyzes the user's utterance and produces a Semantic Request.

Depending on the user's request, the parser produces one of three outcomes:

* Complete Request
* Partial Request
* Conversation

The parser also produces the immediate response that JARVIS should say next.

Examples include:

* "On it."
* "Okay."
* "What would you like to watch?"
* Conversational responses

The Request Parser understands language.

It does not:

* Execute requests.
* Perform routing.
* Resolve references.
* Apply conversation context.
* Determine whether JARVIS supports a capability.

---

## JARVIS Core

JARVIS Core is the heart of the system.

Its responsibilities include:

* Maintaining conversation context.
* Maintaining the current session.
* Routing requests.
* Coordinating plugins.
* Maintaining the capability registry.
* Recording execution history.
* Managing the overall flow of the application.

JARVIS Core understands the architecture of the system but does not understand the implementation details of any specific plugin.

---

## Capability Registry

JARVIS Core maintains a registry of every capability available to the system.

Plugins register the object types and actions they support during initialization.

When a Complete Request is received, JARVIS Core uses the Capability Registry to determine which plugin should handle the request.

If no plugin supports the requested capability, JARVIS Core informs the user that the capability is unavailable.

---

## Plugins

Plugins provide the capabilities of JARVIS.

Each plugin owns a single domain.

Examples include:

* Home Assistant
* Calendar
* TrueNAS
* Email
* Media

A plugin is responsible for:

* Understanding its own domain.
* Resolving references.
* Validating requests.
* Executing actions.
* Returning execution results.

JARVIS Core never attempts to replace this knowledge.

---

## Execution Result Handler

The Execution Result Handler generates responses after plugin execution.

Examples include:

* Reporting failures.
* Reporting warnings.
* Reporting unexpected conditions.
* Providing additional information after execution.

It is not responsible for greetings, conversation, acknowledgements, or clarification questions.

Those responses are generated by the Request Parser before execution begins.

---

# Design Principles

## Single Responsibility

Every component performs one job well.

---

## Separation of Concerns

Language understanding, request routing, execution, and domain knowledge are separate responsibilities.

---

## Parser Extracts Language

The Request Parser extracts language from the user's utterance.

It does not understand the user's environment.

---

## JARVIS Core Owns the Architecture

JARVIS Core manages context, routing, capability discovery, and overall application flow.

---

## Plugins Own Domain Knowledge

Plugins are the authoritative source for their own domain.

Plugins resolve references and execute requests.

---

## Deterministic Information

If JARVIS can determine information directly, it should not ask an AI model to infer it.

Examples include:

* Current time
* Current date
* Current client
* Current room
* Current user
* Device state

---

## Implementation Independence

The Request Parser should not know about plugins.

Plugins should not know about the internals of JARVIS Core.

Each component communicates only through well-defined interfaces.

---

## Extensibility

New capabilities should be added by extending plugins and registering new capabilities.

The routing logic within JARVIS Core should not require modification when adding new capabilities to existing domains.

---

# Request Lifecycle

1. The user interacts with JARVIS through a client.
2. Speech is converted into text if necessary.
3. The Cleanup Preprocessor performs deterministic cleanup.
4. The Fast Response Handler processes predefined deterministic interactions.
5. The Request Parser produces a Semantic Request.
6. JARVIS Core evaluates the parser outcome.
7. If the outcome is **Conversation**, JARVIS returns the parser's message.
8. If the outcome is **Partial Request**, JARVIS returns the parser's clarification question and waits for additional information.
9. If the outcome is **Complete Request**, JARVIS immediately returns the parser's acknowledgement and routes the request through the Capability Registry to the appropriate plugin.
10. The selected plugin resolves references and executes the request.
11. If additional feedback is required after execution, the Execution Result Handler generates the response.

---

# Future Expansion

The architecture is designed so additional capabilities can be added without redesigning the core.

Future enhancements may include:

* Voice identification
* Vision processing
* Learning and personalization
* Mobile applications
* Web dashboards
* Additional plugins
* Additional client types
* New Request Parser implementations
