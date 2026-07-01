# context_engine.md (v0.1)

## 1. Purpose

The Context Engine is responsible for enriching structured requests with known system state, environmental metadata, and session-level information.

Its job is not to interpret intent.

It exists to complete missing information, not to invent new meaning.

---

## 2. What Context Is

Context is any trusted or derived system knowledge that helps resolve incomplete or ambiguous structured requests.

Context includes, but is not limited to:

* Source identity (e.g. ESP32 node)
* Physical location (room, zone, device origin)
* Session state (ongoing interaction memory)
* Device state snapshots
* Recent system events relevant to the request
* Focus object (current topic or target of interaction)

Context is always **external to the request itself**, but may be merged into it.

---

## 3. Context Lifecycle

Context exists in three stages:

### 3.1 Ingestion

Context enters the system from:

* ESP32 nodes
* user input channels
* system events
* external integrations (Home Assistant, sensors, APIs)

### 3.2 Resolution

During request processing, missing fields may be filled using available context.

Example:

* Parsed request: `location = null`
* Context provides: `source_device = esp32_office_01`
* Resolved: `location = office`

### 3.3 Expiration

Context is not permanent by default.

* Session context expires with inactivity
* Device context persists while device is active
* Environmental state is refreshed periodically

No context is assumed to be globally valid unless explicitly defined.

---

## 4. Session Context

Session context represents short-term interaction continuity.

It includes:

* recent commands
* active focus object
* unresolved references (“it”, “that”, “same as before”)
* temporary user preferences for the session

Session context is:

* mutable
* ephemeral
* scoped to a single interaction thread

Session context MUST NOT:

* overwrite persistent system state
* override explicit user input
* be used as permanent memory

---

## 5. Focus Object

The focus object is the current primary entity of interaction.

Examples:

* “living room lights”
* “garage door”
* “music playback session”
* “robot rover control session”

The focus object is derived from:

* most recent explicit command
* session continuation signals
* contextual disambiguation

Rules:

* There is at most one active focus object per session
* Focus is reset when ambiguity cannot be resolved
* Focus does NOT imply intent persistence

---

## 6. Partial Requests

Requests may be incomplete when entering the system.

Example:

* “turn it off”
* parsed: `action=turn_off`, `target=null`

The Context Engine may resolve missing fields using:

* focus object
* last referenced device
* source location
* session context

If no resolution is possible:

* the field remains null
* downstream components must handle ambiguity explicitly

The Context Engine MUST NOT guess beyond available context.

---

## 7. Context Enrichment Rules

The Context Engine may enrich a request with:

* location
* device identity
* session references
* inferred target objects (only from explicit prior references)

Enrichment rules:

* Only fill missing fields
* Never overwrite explicit parsed values
* Never introduce new intent fields
* Never modify action semantics
* Never infer user intent beyond structural completion

Context enrichment is strictly:

> completion, not interpretation

---

## 8. What Context Is NOT

Context is explicitly NOT allowed to:

* determine user intent
* resolve ambiguous meaning beyond structural disambiguation
* choose between multiple valid actions
* introduce new commands or capabilities
* override parsed semantic request fields
* persist long-term behavioral assumptions without explicit storage layer approval

Context is not intelligence.

It is **reference memory + environmental truth injection**.

---

## 9. Boundary With Semantic Request

The Semantic Request defines:

* what the user meant structurally

The Context Engine provides:

* missing structural pieces

The Context Engine MUST NOT:

* reinterpret intent
* change action type
* alter semantic classification

If Semantic Request says:

```json
{ "action": "play_music" }
```

Context Engine may add:

```json
{ "location": "office" }
```

It may NOT change:

```json
{ "action": "stream_spotify_playlist" } 
```

---

## 10. Failure Behavior

If context is:

* missing
* conflicting
* ambiguous

Then:

* do not resolve
* pass null forward
* mark field as `unresolved_context`

No guessing is allowed under failure conditions.

---

## 11. Philosophy Summary

The Context Engine is:

> a lens that sharpens incomplete requests using known reality

It is NOT:

* reasoning
* memory
* intent prediction
* or decision-making

It is the system’s:

> grounding layer — nothing more, nothing less
