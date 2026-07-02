## 1. Overview

This document describes the current architecture of the Jarvis audio ingestion system. The system is designed to receive raw audio streams from distributed ESP32 devices, buffer them per device, and persist them as WAV files for later processing.

The design follows a strict separation of concerns:

* Transport layer (WebSocket)
* Message routing layer
* Audio processing layer
* Device registry layer

---

## 2. Repository Structure

```text
jarvis-core/
│
├── __main__.py
│
├── websocket/
│   ├── server.py
│   └── websocket_handler.py
│
├── audio/
│   ├── receiver.py
│   └── wav_writer.py
│
├── devices/
│   └── registry.py
│
└── data/
```

The `data/` directory is a runtime output directory intended for WAV file persistence.

---

## 3. System Data Flow

```text
ESP32 Device
  ↓
WebSocket Connection
  ↓
websocket_handler.py
  ↓
audio/receiver.py
  ↓
audio/wav_writer.py
  ↓
WAV files stored in /data
```

---

## 4. Component Specifications

---

### 4.1 websocket/server.py

**Responsibility**

Initializes the WebSocket server and background tasks.

**Inputs**

* None (process entry point)

**Outputs**

* Running WebSocket server on port 8765

**Dependencies**

* websocket_handler.websocket_handler
* audio.receiver.session_flusher

**Behavior**

* Starts asynchronous WebSocket server
* Launches background session flusher task
* Does not process messages directly

---

### 4.2 websocket/websocket_handler.py

**Responsibility**

Parses and routes all incoming WebSocket messages.

**Inputs**

* Binary frames (audio PCM)
* JSON control messages

**Outputs**

* Calls into:

  * audio.receiver.receive_audio
  * devices.registry.register_device
  * devices.registry.unregister_device
  * devices.registry.export_devices

**Behavior**

* Maintains per-connection device identity
* Routes binary payloads to audio subsystem
* Routes JSON messages to appropriate handlers
* Does not store audio state

---

### 4.3 audio/receiver.py

**Responsibility**

Manages per-device audio buffering and session lifecycle.

**Inputs**

* device_id (string)
* audio_bytes (PCM 16-bit mono)

**Outputs**

* Calls audio.wav_writer.write_wav
* Maintains in-memory buffers
* Writes WAV files to disk via flush process

**Behavior**

* Maintains a dictionary of active device buffers
* Tracks last activity timestamp per device
* Runs background coroutine that flushes inactive sessions
* Flush condition: inactivity timeout (currently 2 seconds)

---

### 4.4 audio/wav_writer.py

**Responsibility**

Converts raw PCM audio into WAV format and persists to disk.

**Inputs**

* filename (string)
* pcm_bytes (bytes)
* sample_rate (default: 16000 Hz)

**Outputs**

* WAV file written to disk

**Behavior**

* Stateless utility module
* Performs no buffering or interpretation

---

### 4.5 devices/registry.py

**Responsibility**

Maintains active device connections and metadata.

**Inputs**

* device_id
* websocket connection
* metadata payload

**Outputs**

* Registry of active devices
* Device list responses

**Behavior**

* Registers devices on connection
* Unregisters devices on disconnect
* Provides list of active devices

---

## 5. Communication Contracts

### 5.1 Audio Stream (ESP32 → Server)

* Transport: WebSocket binary frame
* Format: PCM 16-bit mono
* Sample rate: 16000 Hz

No framing or headers are included in the stream.

---

### 5.2 Device Registration Message

```json
{
  "type": "register",
  "device_id": "kitchen",
  "metadata": {}
}
```

---

### 5.3 Device List Request

```json
{
  "type": "list_devices"
}
```

---

## 6. Session Lifecycle

### 6.1 Device Lifecycle

1. WebSocket connection established
2. Device registration message received
3. Audio streaming begins
4. Inactivity threshold reached
5. Session flushed to WAV
6. Device disconnect triggers cleanup

---

### 6.2 Audio Session Lifecycle

1. Audio bytes received via WebSocket
2. Appended to per-device buffer
3. Timestamp updated
4. Background flusher evaluates inactivity
5. Buffer is flushed to WAV if inactive
6. Buffer is reset

---

## 7. Design Constraints

* WebSocket layer does not process audio content
* Audio subsystem does not handle networking
* Device registry does not process audio or files
* All modules are designed to be independently replaceable

---

## 8. Extension Points

The architecture is designed to support future modules without modification to existing components:

* Voice Activity Detection (VAD)
* Wake word detection
* Speech-to-text processing
* Intent classification
* Home automation action layer
