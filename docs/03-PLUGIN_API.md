## 1. Purpose

The Plugin API defines how Jarvis executes external capabilities through a standardized, deterministic interface.

Plugins are execution endpoints only.
They do not interpret language, make decisions, or manage system state.

All reasoning is handled by upstream components. Plugins strictly execute validated actions.

---

## 2. Core Principles

* **Deterministic execution**: same input → same output behavior
* **No embedded reasoning**: plugins do not interpret intent
* **Explicit contracts only**: all inputs and outputs are schema-defined
* **Failure is data**: errors are returned, not handled internally
* **Stateless execution preferred**: plugins should avoid hidden state

---

## 3. Plugin Definition

Each plugin MUST declare a manifest:

```json
{
  "id": "string",
  "version": "semver",
  "description": "string",
  "capabilities": ["string"],
  "auth": {
    "type": "none | token | oauth | custom",
    "config": {}
  },
  "entrypoint": "string",
  "timeout_ms": 5000
}
```

### Rules

* `id` must be globally unique
* `capabilities` define executable functions exposed by the plugin
* `entrypoint` is the base execution target (HTTP, MQTT, local function bridge, etc.)

---

## 4. Capability Model

A plugin exposes one or more capabilities.

Each capability is a strictly typed function:

```json
{
  "name": "light_control",
  "description": "Control lights in a specified location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": { "type": "string" },
      "state": { "type": "string", "enum": ["on", "off", "toggle"] },
      "brightness": { "type": "integer", "minimum": 0, "maximum": 100 }
    },
    "required": ["location", "state"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "message": { "type": "string" }
    }
  }
}
```

### Rules

* Input schema MUST be validated before execution
* Output schema MUST be returned even on failure
* No dynamic or inferred fields allowed

---

## 5. Execution Contract

All plugin execution follows this structure:

### Request

```json
{
  "plugin_id": "home_assistant",
  "capability": "light_control",
  "request_id": "uuid",
  "timestamp": "iso-8601",
  "context": {
    "room": "kitchen",
    "source": "esp32_kitchen_01",
    "user": "optional"
  },
  "input": {}
}
```

---

### Response

```json
{
  "request_id": "uuid",
  "status": "success | failure",
  "output": {},
  "error": {
    "code": "optional",
    "message": "optional"
  },
  "latency_ms": 123
}
```

---

## 6. Execution Rules

* Plugins MUST NOT modify request structure
* Plugins MUST NOT call other plugins
* Plugins MUST return within `timeout_ms`
* Plugins MUST always return a response object
* Silent failure is forbidden

---

## 7. Error Handling

All errors are returned explicitly:

```json
{
  "status": "failure",
  "error": {
    "code": "DEVICE_OFFLINE",
    "message": "Kitchen light not reachable"
  }
}
```

### Standard error codes (initial set)

* `INVALID_INPUT`
* `UNAUTHORIZED`
* `TIMEOUT`
* `DEVICE_OFFLINE`
* `UNSUPPORTED_CAPABILITY`

---

## 8. Context Handling

Plugins may receive contextual metadata but MUST NOT depend on it for correctness unless explicitly required.

Allowed context fields:

* room
* source device
* user id
* system state snapshot (optional)

Plugins MUST ignore unknown context fields.

---

## 9. Security Model

* Plugins are isolated execution units
* No plugin has access to filesystem or runtime outside its scope unless explicitly granted
* Authentication is enforced at dispatcher level, not plugin level (preferred)

---

## 10. Versioning

* Plugin versions follow semantic versioning
* Capability changes that break schema MUST increment major version
* Backward compatibility is optional, not guaranteed unless declared

---

## 11. Philosophy Summary

Plugins are:

> “dumb hands that do exactly what the brain already decided”

They are NOT:

* interpreters
* agents
* mini assistants

They are:

> controlled actuators in a structured cognitive system

