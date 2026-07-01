# 📄 Context Engine — Core Definition (drop-in)

## 1. Purpose

The Context Engine is a **deterministic enrichment system** that fills missing or implicit fields in a Semantic Request using structured system context.

It does not interpret user intent and does not validate real-world entities.

It operates only on:

* session context
* device metadata (ESP32 location tags)
* focus object
* recent action history (session-scoped)

---

## 2. What Context Is

Context is defined as:

> Any non-explicit information that helps complete a partially specified Semantic Request without altering its semantic meaning.

This includes:

* location (from ESP32 source)
* last known device interaction (session history)
* focus object
* temporal session state (recent actions)

---

## 3. What Context is NOT

The Context Engine MUST NOT:

* decide user intent
* select between multiple ambiguous targets without deterministic rules
* invent new entities
* normalize targets into “known device truth”
* query external systems (Home Assistant, plugins, etc.)
* override explicit Semantic Request fields

If a field is explicit, it is immutable.

---

## 4. Inputs

Context Engine receives:

### 4.1 Semantic Request

Structured object containing:

* action
* target (possibly null)
* parameters

---

### 4.2 Session Context

* focus object
* recent actions (ordered list)
* last resolved device per category

---

### 4.3 Device Origin Context

* ESP32 ID
* physical location mapping (room)

---

## 5. Output Rules

Context Engine returns:

* same Semantic Request
* with ONLY missing fields filled

It MUST NOT:

* modify existing non-null fields
* rewrite target strings
* rename objects

---

## 6. Focus Object Rule

If:

```text
target == null
```

Then resolution order is:

1. Focus Object (if valid)
2. Same-room last active device
3. Session last referenced device
4. ESP32-origin inferred device context
5. unresolved → leave null

If multiple candidates exist at a level:
→ DO NOT resolve (pass upward unchanged)

---

## 7. Temporal Resolution (Session History)

Session history is:

* ordered list of successful device actions only

Used ONLY when:

* target is null
* focus object is null or invalid

Selection rule:

> most recent valid action within same context scope

Scope priority:

1. same room (highest)
2. same device type
3. global session (lowest)

---

## 8. Determinism Rule (IMPORTANT)

Context Engine MUST be deterministic.

Given identical input state:

> output MUST always be identical

No randomness, heuristics, or probabilistic selection allowed.

---

## 9. Failure Behavior

If Context Engine cannot resolve a missing field:

* it MUST leave the field null
* it MUST NOT guess
* it MUST NOT infer multiple candidates into one choice

Unresolved ambiguity is valid output.

---

## 10. Interaction Rules

### 10.1 With Semantic Request

* only fills null fields
* never modifies explicit fields

### 10.2 With Jarvis Core

* Jarvis consumes enriched request
* Context Engine does not route or execute

### 10.3 With Home Assistant

* Context Engine has no knowledge of HA devices

---

## 11. Summary Model

Context Engine is:

> a deterministic, session-aware field completion system with strict non-inference rules

NOT:

* reasoning engine
* intent resolver
* device selector
* knowledge system
