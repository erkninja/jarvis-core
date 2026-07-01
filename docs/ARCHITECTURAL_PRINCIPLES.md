## Parser extracts language.

The Request Parser extracts language and structure from the user's utterance.

It does not understand the user's environment, choose plugins, resolve devices, or execute actions.

---

## JARVIS Core owns architecture.

JARVIS Core coordinates the system.

It manages routing, context, sessions, capability registration, execution flow, and trace recording.

---

## Plugins own domain knowledge.

Plugins are responsible for understanding and interacting with their own domains.

For example:

* Home Assistant understands lights, locks, rooms, and devices.
* Calendar understands calendars, events, and tasks.
* TrueNAS understands pools, datasets, and services.

---

## Deterministic knowledge does not come from AI.

If JARVIS can determine something directly, it should not ask an AI model to infer it.

Examples:

* Current time
* Current date
* Current room
* Current user
* Device state
* Registered capabilities

---

## Null means unknown.

A `null` value means the parser could not determine the value from the user's utterance.

It does not mean default, current, assumed, or unsupported.

---

## The parser may acknowledge, but not confirm success.

For complete requests, the parser may return messages such as:

* "On it."
* "Okay."
* "Sure thing."

It must not say or imply that execution succeeded before JARVIS Core and the plugin complete the action.

---

## Plugins resolve references.

The parser may extract:

```text
object.type = light
object.reference = desk lamp
location = kids room
```

The responsible plugin resolves that into the correct device, entity, calendar, service, or resource.

---

## JARVIS learns only from confirmation.

Future learning features may suggest aliases, preferences, or configuration updates.

Permanent behavior changes must require explicit user confirmation.

---

## Everything should be traceable.

Every interaction should produce enough trace data to understand:

* What the user said
* What the parser returned
* How JARVIS routed the request
* What plugin executed it
* What happened

---

## Earn complexity.

Do not introduce abstractions, components, fields, or processes until they solve a demonstrated problem.

Prefer the simplest design that satisfies the current requirements.
