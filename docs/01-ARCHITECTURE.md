JARVIS Core

01 - Architecture

Overview

JARVIS is composed of small, independent components that each perform a single responsibility.

No component should understand another component’s implementation details.

Each component communicates through well-defined interfaces.

⸻

High-Level Architecture

                  Client
       (ESP32, Web, Mobile, API)
                     │
          Speech Recognition
             (if voice input)
                     │
             Semantic Parser
                 (LLM)
                     │
          Semantic Request
                     │
              JARVIS Core
     ┌────────────┼────────────┐
     │            │            │
 Context      Router      Trace Recorder
 Engine
                     │
             Object Registry
                     │
          Appropriate Plugin
                     │
        Resolve → Execute
                     │
            Execution Result
                     │
          Personality Engine
                     │
            Speech / Text Reply

⸻

Component Responsibilities

Speech Recognition

Responsibilities

* Convert audio into text.

Examples

* Whisper
* Faster Whisper

Speech Recognition does not understand intent.

⸻

Semantic Parser

Responsibilities

* Understand natural language.
* Produce a Semantic Request.

The parser never executes requests.

The parser never understands plugins.

The parser never understands APIs.

The parser never understands Home Assistant.

It only understands language.

⸻

JARVIS Core

Responsibilities

* Receive Semantic Requests.
* Maintain conversation state.
* Route requests.
* Coordinate plugins.
* Record traces.
* Generate responses.

JARVIS Core owns the application.

⸻

Context Engine

Responsibilities

Maintain conversational state.

Examples

* Current conversation
* Previous requests
* Current room
* Current user
* Focus object
* Session ownership

The Context Engine supplies information that was not explicitly spoken.

⸻

Router

Responsibilities

Determine which plugin owns the requested object.

Example

Light
    ↓
Home Assistant Plugin
Calendar
    ↓
Calendar Plugin
Storage
    ↓
TrueNAS Plugin

Routing is deterministic.

The Semantic Parser never selects plugins.

⸻

Object Registry

The Object Registry maps object types to plugins.

Example

Light
Lock
Climate
Media Player
↓
Home Assistant Plugin
Calendar
Todo List
↓
Calendar Plugin
Storage
Dataset
Pool
↓
TrueNAS Plugin

The registry allows plugins to be replaced without modifying the Semantic Parser.

⸻

Plugins

Each plugin owns a single domain.

Responsibilities

* Resolve references.
* Validate requests.
* Execute actions.
* Return results.

Examples

Home Assistant Plugin

* Lights
* Locks
* Climate
* Sensors
* Media Players

Calendar Plugin

* Calendars
* Events
* Tasks

TrueNAS Plugin

* Pools
* Datasets
* Services

Plugins are authoritative for their domain.

⸻

Trace Recorder

Every request should produce a trace.

A trace contains

* Original transcript
* Semantic Request
* Routing decision
* Resolution
* Execution
* Result
* Response

Trace data supports

* Debugging
* Analytics
* Testing
* Future improvements

⸻

Personality Engine

Responsibilities

Convert execution results into natural responses.

Examples

Execution Result

Light turned on.

Possible responses

“Done.”

“Certainly.”

“The office lights are now on.”

Personality never affects execution.

⸻

Design Principles

The architecture follows these rules.

1. Components have a single responsibility.
2. The Semantic Parser understands language.
3. JARVIS Core understands architecture.
4. Plugins understand their domain.
5. Plugins resolve resources.
6. The Context Engine owns conversation state.
7. The Personality Engine owns communication.
8. Every request is traceable.

⸻

Request Lifecycle

User speaks
↓
Speech Recognition
↓
Semantic Parser
↓
Semantic Request
↓
Context Engine
(add context)
↓
Router
↓
Plugin
↓
Resolve
↓
Execute
↓
Execution Result
↓
Trace Recorder
↓
Personality Engine
↓
Response

⸻

Future Components

These are outside the scope of Version 1 but should integrate without changing the architecture.

* Voice Identification
* Learning Engine
* Alias Manager
* Proactive Notifications
* Vision Processing
* Multi-Agent Planning
* Mobile Client
* Web Dashboard
* Automation Engine