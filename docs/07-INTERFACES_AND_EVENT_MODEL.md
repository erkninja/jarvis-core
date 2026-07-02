## 1. Module Interface Contracts

This section defines the **function-level contracts** between modules. These are treated as stable APIs within the system.

---

## 1.1 websocket/server.py

### Interface

```python id="i_srv_1"
async def start_server() -> None
```

### Responsibilities

* Initialize WebSocket server
* Start background tasks
* Bind handler to incoming connections

### Calls

* `websocket.websocket_handler.websocket_handler`
* `audio.receiver.session_flusher`

### Constraints

* Must not process messages
* Must not access audio buffers

---

## 1.2 websocket/websocket_handler.py

### Interface

```python id="i_wh_1"
async def websocket_handler(websocket) -> None
```

### Internal Responsibilities

* Parse incoming WebSocket frames
* Maintain per-connection device identity
* Route messages to subsystem APIs

### Outgoing Calls

```python id="i_wh_2"
receive_audio(device_id: str, audio_bytes: bytes) -> None
register_device(device_id: str, websocket, metadata: dict) -> None
unregister_device(device_id: str) -> None
export_devices() -> dict
```

### Input Types

#### Binary Frame

```text id="i_wh_3"
bytes (PCM audio)
```

#### JSON Frame

```json id="i_wh_4"
{
  "type": "register" | "list_devices",
  "device_id": "string (optional)",
  "metadata": "object (optional)"
}
```

---

## 1.3 audio/receiver.py

### Interfaces

```python id="i_ar_1"
def receive_audio(device_id: str, audio_bytes: bytes) -> None
```

```python id="i_ar_2"
async def session_flusher() -> None
```

```python id="i_ar_3"
def flush_session(device_id: str) -> None
```

### Internal State

```python id="i_ar_4"
sessions: dict[str, AudioSession]
```

Where:

```python id="i_ar_5"
AudioSession = {
    "buffer": bytearray,
    "last_update": float
}
```

### Behavior

* Buffers audio per device
* Tracks last activity timestamp
* Triggers flush based on inactivity threshold
* Delegates file writing to `wav_writer`

### Outputs

* Calls `write_wav(...)`
* Emits file to `/data`

---

## 1.4 audio/wav_writer.py

### Interface

```python id="i_aw_1"
def write_wav(filename: str, pcm_bytes: bytes, sample_rate: int = 16000) -> None
```

### Behavior

* Converts PCM → WAV container
* Writes file to disk
* Stateless operation

### Constraints

* No buffering
* No session awareness
* No device context

---

## 1.5 devices/registry.py

### Interfaces

```python id="i_dr_1"
def register_device(device_id: str, websocket, metadata: dict) -> None
def unregister_device(device_id: str) -> None
def export_devices() -> dict
```

### Internal State

```python id="i_dr_2"
devices: dict[str, Device]
```

---

# 2. Event Model

This section defines the **logical events** flowing through the system. These are not physical classes yet, but they represent the intended runtime contract.

---

## 2.1 Event: ConnectionEstablished

```text id="e_1"
Source: ESP32
Target: websocket_handler
Trigger: WebSocket open
```

No payload.

---

## 2.2 Event: DeviceRegistered

```json id="e_2"
{
  "type": "DeviceRegistered",
  "device_id": "kitchen",
  "metadata": {}
}
```

Emitted after successful register message.

---

## 2.3 Event: AudioFrameReceived

```text id="e_3"
Source: ESP32
Transport: WebSocket binary frame
Payload: PCM16 mono @ 16kHz
```

This event is emitted for every incoming audio chunk.

### Handling Path

```
websocket_handler
  → receive_audio(device_id, bytes)
      → append to session buffer
```

---

## 2.4 Event: SessionUpdated

```json id="e_4"
{
  "type": "SessionUpdated",
  "device_id": "kitchen",
  "buffer_size": 4096,
  "last_update": 1234567890.0
}
```

Internal event (not currently emitted externally, but defined for future observability).

---

## 2.5 Event: SessionExpired

```json id="e_5"
{
  "type": "SessionExpired",
  "device_id": "kitchen"
}
```

Trigger condition:

* `now - last_update > 2 seconds`

---

## 2.6 Event: AudioSessionFlushed

```json id="e_6"
{
  "type": "AudioSessionFlushed",
  "device_id": "kitchen",
  "file_path": "/data/kitchen_123456.wav",
  "duration_estimate_sec": 2-5
}
```

Emitted after:

```
flush_session()
  → write_wav()
```

---

# 3. System State Machine (Per Device)

```text id="s_1"
[Disconnected]
    ↓
[Connected]
    ↓
[Registered]
    ↓
[Streaming Audio]
    ↓
[Idle Timer Running]
    ↓
[Session Flush]
    ↓
[Streaming Audio]
```

---

# 4. Key Architectural Rule (Formalized)

## Responsibility Boundary Rule

Each subsystem owns exactly one concern:

* websocket layer → transport only
* handler layer → routing only
* audio layer → buffering + session logic
* wav writer → file serialization
* registry → device identity

No module is allowed to:

* interpret audio meaning
* make session decisions outside its boundary
* perform cross-domain logic

---

# 5. Forward Compatibility Notes

This event model is designed so that future components can attach without modifying existing modules:

### Future additions:

* `AudioFrameReceived → VAD → SessionStart/End`
* `SessionExpired → STT pipeline`
* `AudioSessionFlushed → transcription queue`
* `DeviceRegistered → capability negotiation`
