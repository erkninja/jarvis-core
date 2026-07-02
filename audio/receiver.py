from pathlib import Path
import asyncio
import time

from audio.wav_writer import write_wav

DATA_DIR = Path("/app/data")

# ------------------------------------------------------------------
# Active audio sessions
#
# sessions = {
#     "kitchen": {
#         "buffer": bytearray(),
#         "last_update": 1234567890.0
#     }
# }
# ------------------------------------------------------------------
sessions = {}


# ------------------------------------------------------------------
# Receive audio from a device
# ------------------------------------------------------------------
def receive_audio(device_id, audio_bytes):
    now = time.time()

    if device_id not in sessions:
        sessions[device_id] = {
            "buffer": bytearray(),
            "last_update": now
        }

    session = sessions[device_id]

    session["buffer"].extend(audio_bytes)
    session["last_update"] = now

    print(
        f"[Audio] {device_id}: +{len(audio_bytes)} bytes "
        f"(total {len(session['buffer'])})"
    )


# ------------------------------------------------------------------
# Background task
#
# Flushes audio after 2 seconds of inactivity.
#
# This is only a temporary Round 1 implementation.
# Later this will become wake-word/session based.
# ------------------------------------------------------------------
async def session_flusher():

    while True:

        now = time.time()

        to_flush = []

        for device_id, session in sessions.items():

            if now - session["last_update"] > 2.0:
                to_flush.append(device_id)

        for device_id in to_flush:
            flush_session(device_id)

        await asyncio.sleep(1)


# ------------------------------------------------------------------
# Flush one completed session
# ------------------------------------------------------------------
def flush_session(device_id):

    session = sessions.pop(device_id, None)

    if session is None:
        return

    raw_data = session["buffer"]

    if len(raw_data) == 0:
        return

    filename = DATA_DIR / f"{device_id}_{int(time.time())}.wav"

    write_wav(str(filename), raw_data)

    print(f"[Audio] Wrote WAV: {filename}")
