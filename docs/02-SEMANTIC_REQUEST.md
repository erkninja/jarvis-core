# 02 - Semantic Request

## Purpose

A Semantic Request is the structured result produced from a user's utterance.

It is the contract between the Request Parser and JARVIS Core.

A Semantic Request describes what the user said and what JARVIS should say next.

---

# Scope

A Semantic Request contains only information that can be extracted directly from the user's utterance.

It does not contain:

* Plugin names
* API details
* Entity IDs
* Device IDs
* Home Assistant concepts
* Calendar IDs
* Routing information
* Contextual defaults

Those responsibilities belong to JARVIS Core and the appropriate plugin.

---

# Semantic Request Structure

Every response from the Request Parser shall conform to the following structure.

| Field    | Description                                                             | Required |
| -------- | ----------------------------------------------------------------------- | :------: |
| Outcome  | The parser's determination of what should happen next.                  |    Yes   |
| Subject  | The person or group explicitly referenced by the user.                  |    No    |
| Object   | The resource being acted upon. Consists of a type and a user reference. |    No    |
| Action   | The operation requested by the user.                                    |    No    |
| Location | A location explicitly mentioned by the user.                            |    No    |
| Time     | A time explicitly mentioned by the user.                                |    No    |
| Message  | The immediate response JARVIS should say next.                          |    Yes   |

### Example Structure

```json
{
  "outcome": "complete_request",
  "subject": null,
  "object": {
    "type": "light",
    "reference": "desk lamp"
  },
  "action": "turn_on",
  "location": "Kids Room",
  "time": null,
  "message": "On it."
}
```

---

# Parser Outcomes

Every Semantic Request must have one of the following outcomes.

## Complete Request

A Complete Request contains enough information for JARVIS Core to attempt execution.

For a Complete Request:

* `outcome` is `complete_request`
* `action` must not be `null`
* `object` should not be `null`
* `message` must contain a short acknowledgement
* `message` must not imply the action has succeeded

Examples of valid messages:

* "On it."
* "Okay."
* "Sure thing."
* "I'll work on that."

---

## Partial Request

A Partial Request means the parser understands the general request, but more information is needed before JARVIS can continue.

For a Partial Request:

* `outcome` is `partial_request`
* Missing fields should be `null`
* `message` must contain a concise follow-up question
* JARVIS Core may return `message` directly to the user without making another AI call

Example:

```json
{
  "outcome": "partial_request",
  "subject": null,
  "object": {
    "type": "media",
    "reference": "movie"
  },
  "action": null,
  "location": null,
  "time": null,
  "message": "What would you like to watch?"
}
```

---

## Conversation

A Conversation outcome means the utterance does not require plugin execution.

For a Conversation outcome:

* `outcome` is `conversation`
* `action` must be `null`
* `message` must contain the response to return to the user

Example:

```json
{
  "outcome": "conversation",
  "subject": null,
  "object": {
    "type": "vehicle",
    "reference": "2014 Mazda3s"
  },
  "action": null,
  "location": null,
  "time": null,
  "message": "The top speed depends on the exact trim and conditions, but a 2014 Mazda3s is generally reported around the low-130 mph range."
}
```

---

# Field Definitions

## Outcome

### Description

The parser's determination of what should happen next.

### Allowed Values

* `complete_request`
* `partial_request`
* `conversation`

### Rules

* Every Semantic Request must include an outcome.
* The outcome determines how JARVIS Core handles the request.
* The parser must not use the outcome to indicate whether JARVIS supports a capability.
* Unsupported capabilities are determined later by JARVIS Core.

---

## Subject

### Description

The person or group explicitly referenced by the user.

### Examples

* me
* Eric
* household
* everyone

### Rules

* Only include a subject if it is explicitly stated or directly implied by the user's words.
* "I", "me", and "my" may map to `me`.
* "We", "us", and "our" may map to `household`.
* Do not infer a default subject.
* Use `null` if no subject is present.

---

## Object

### Description

The resource involved in the request.

Every object consists of:

* Type
* Reference

### Object Structure

| Field     | Description                                                | Required |
| --------- | ---------------------------------------------------------- | :------: |
| Type      | The category of resource. Used by JARVIS Core for routing. |    Yes   |
| Reference | The words used by the user to identify the resource.       |    No    |

### Examples

| Type     | Reference     |
| -------- | ------------- |
| light    | desk lamp     |
| light    | room lights   |
| calendar | work calendar |
| media    | Plex          |
| storage  | NAS           |

### Rules

* `type` should be a canonical resource category.
* `reference` should preserve the user's wording whenever practical.
* The parser does not determine whether the reference actually exists.
* The parser does not resolve references to specific devices, entities, calendars, or services.

---

## Action

### Description

The operation requested by the user.

### Examples

* turn_on
* turn_off
* set_brightness
* play
* pause
* restart
* get_schedule
* add_item

### Rules

* The action should use a canonical action name.
* The parser may normalize natural language verbs into canonical actions.
* Do not include implementation-specific action names.
* Use `null` when no executable action is present or when the request is incomplete.

Example:

| User Says            | Action   |
| -------------------- | -------- |
| Turn off the lights. | turn_off |
| Shut the lights.     | turn_off |
| Kill the lights.     | turn_off |

---

## Location

### Description

A location explicitly mentioned by the user.

### Examples

* Kitchen
* Office
* Kids Room
* Upstairs
* Outside

### Rules

* Preserve the user's wording.
* Do not determine whether the location is an Area, Floor, Zone, or alias.
* Use `null` if no location is explicitly stated.
* Do not infer the current room.

---

## Time

### Description

A time explicitly mentioned by the user.

### Examples

* now
* today
* tomorrow
* 5 PM
* sunset

### Rules

* Preserve the user's wording.
* Do not resolve relative times into absolute values.
* Use `null` if no time is explicitly stated.
* Do not infer the current time.

---

## Message

### Description

The immediate response JARVIS should say next.

### Rules

* For `complete_request`, `message` must contain a short acknowledgement.
* For `complete_request`, `message` must not imply the action has succeeded.
* For `partial_request`, `message` must contain a follow-up question.
* For `conversation`, `message` must contain the conversational response.
* `message` may be spoken before plugin execution occurs.

---

# Parser Rules

The Request Parser shall:

* Extract only information contained within the user's utterance.
* Preserve user terminology whenever practical.
* Normalize actions into canonical action names.
* Return `null` for unknown values.
* Produce the same structure for every parser response.
* Produce an immediate user-facing `message`.

The Request Parser shall not:

* Guess missing information.
* Apply conversational context.
* Resolve references.
* Select plugins.
* Perform routing.
* Execute requests.
* Infer implementation details.
* Determine whether JARVIS supports a capability.
* Claim that an action succeeded before execution.

---

# Unknown Values

A value of `null` means the Request Parser could not determine that information from the user's utterance.

`null` does not imply:

* Current room
* Current user
* Current time
* Default values
* Unsupported capability

JARVIS Core may enrich the request with contextual information after parsing.

---

# Capability Support

The Request Parser does not determine whether JARVIS can perform a requested action.

For example, if the user says:

> Turn on the sprinklers.

The parser may return a Complete Request:

```json
{
  "outcome": "complete_request",
  "subject": null,
  "object": {
    "type": "sprinkler",
    "reference": "sprinklers"
  },
  "action": "turn_on",
  "location": null,
  "time": null,
  "message": "On it."
}
```

JARVIS Core is responsible for determining whether a registered plugin can handle `sprinkler`.

---

# Response Requirements

Every Request Parser implementation must:

* Return the same Semantic Request structure.
* Return the same field names.
* Return the same field types.
* Represent unknown values as `null`.
* Return only the Semantic Request.
* Never include implementation-specific information.

---

# Examples

| User Utterance                           | Outcome          | Subject   | Object Type | Object Reference | Action          | Location  | Time             | Message                                                                                                                        |
| ---------------------------------------- | ---------------- | --------- | ----------- | ---------------- | --------------- | --------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Turn on the lights.                      | complete_request | null      | light       | lights           | turn_on         | null      | null             | On it.                                                                                                                         |
| Turn on the room lights.                 | complete_request | null      | light       | room lights      | turn_on         | null      | null             | Okay.                                                                                                                          |
| Turn on the desk lamp.                   | complete_request | null      | light       | desk lamp        | turn_on         | null      | null             | Sure thing.                                                                                                                    |
| Turn on the desk lamp in the kids' room. | complete_request | null      | light       | desk lamp        | turn_on         | Kids Room | null             | On it.                                                                                                                         |
| Shut the lights.                         | complete_request | null      | light       | lights           | turn_off        | null      | null             | Okay.                                                                                                                          |
| Turn off all the lights upstairs.        | complete_request | null      | light       | all lights       | turn_off        | upstairs  | null             | Sure thing.                                                                                                                    |
| Dim the lights to 50%.                   | complete_request | null      | light       | lights           | set_brightness  | null      | null             | On it.                                                                                                                         |
| Make the lights blue.                    | complete_request | null      | light       | lights           | set_color       | null      | null             | Okay.                                                                                                                          |
| Lock the front door.                     | complete_request | null      | lock        | front door       | lock            | null      | null             | On it.                                                                                                                         |
| Unlock the back door tomorrow morning.   | complete_request | null      | lock        | back door        | unlock          | null      | tomorrow morning | Okay.                                                                                                                          |
| Open the garage door.                    | complete_request | null      | garage_door | garage door      | open            | null      | null             | Sure thing.                                                                                                                    |
| Close the blinds in the office.          | complete_request | null      | blinds      | blinds           | close           | Office    | null             | On it.                                                                                                                         |
| Set the thermostat to 70 degrees.        | complete_request | null      | thermostat  | thermostat       | set_temperature | null      | null             | Okay.                                                                                                                          |
| Play jazz.                               | complete_request | null      | media       | jazz             | play            | null      | null             | On it.                                                                                                                         |
| Play jazz in the kitchen.                | complete_request | null      | media       | jazz             | play            | Kitchen   | null             | Sure thing.                                                                                                                    |
| Pause the TV.                            | complete_request | null      | media       | TV               | pause           | null      | null             | Okay.                                                                                                                          |
| Restart Plex.                            | complete_request | null      | media       | Plex             | restart         | null      | null             | On it.                                                                                                                         |
| I want to watch a movie.                 | partial_request  | null      | media       | movie            | null            | null      | null             | What would you like to watch?                                                                                                  |
| What's on my calendar today?             | complete_request | me        | calendar    | my calendar      | get_schedule    | null      | today            | On it.                                                                                                                         |
| What's on the family calendar?           | complete_request | household | calendar    | family calendar  | get_schedule    | null      | null             | Sure thing.                                                                                                                    |
| What do I have to do tomorrow?           | complete_request | me        | calendar    | calendar         | get_schedule    | null      | tomorrow         | Okay.                                                                                                                          |
| What do we have to do this weekend?      | complete_request | household | calendar    | calendar         | get_schedule    | null      | this weekend     | On it.                                                                                                                         |
| Add milk to the shopping list.           | complete_request | null      | todo_list   | shopping list    | add_item        | null      | null             | Sure thing.                                                                                                                    |
| Mark laundry as complete.                | complete_request | null      | todo_item   | laundry          | complete        | null      | null             | Okay.                                                                                                                          |
| What's the weather tomorrow?             | complete_request | null      | weather     | weather          | get_forecast    | null      | tomorrow         | On it.                                                                                                                         |
| Will it rain this afternoon?             | complete_request | null      | weather     | weather          | get_forecast    | null      | this afternoon   | Sure thing.                                                                                                                    |
| How much storage is left?                | complete_request | null      | storage     | storage          | get_usage       | null      | null             | On it.                                                                                                                         |
| How much space is left on the NAS?       | complete_request | null      | storage     | NAS              | get_usage       | null      | null             | Okay.                                                                                                                          |
| Start a scrub on the main pool.          | complete_request | null      | storage     | main pool        | start_scrub     | null      | null             | On it.                                                                                                                         |
| Restart the Jellyfin service.            | complete_request | null      | service     | Jellyfin         | restart         | null      | null             | Sure thing.                                                                                                                    |
| Reboot the NAS tonight.                  | complete_request | null      | system      | NAS              | reboot          | null      | tonight          | Okay.                                                                                                                          |
| What is the top speed of a 2014 Mazda3s? | conversation     | null      | vehicle     | 2014 Mazda3s     | null            | null      | null             | The top speed depends on the exact trim and conditions, but a 2014 Mazda3s is generally reported around the low-130 mph range. |
| Thank you.                               | conversation     | null      | null        | null             | null            | null      | null             | You're welcome.                                                                                                                |
| Hello.                                   | conversation     | null      | null        | null             | null            | null      | null             | Hello.                                                                                                                         |
| Good morning.                            | conversation     | null      | null        | null             | null            | null      | null             | Good morning.                                                                                                                  |
| Never mind.                              | conversation     | null      | null        | null             | null            | null      | null             | Okay.                                                                                                                          |
| Stop.                                    | conversation     | null      | null        | null             | null            | null      | null             | Stopping.                                                                                                                      |
