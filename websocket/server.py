import asyncio
import websockets

from audio.receiver import session_flusher
from websocket.websocket_handler import websocket_handler


# --------------------------------------------------
# Start WebSocket Server
# --------------------------------------------------
async def start_server():

    # Start background audio flusher
    asyncio.create_task(session_flusher())

    print("[Jarvis] WebSocket listening on :8765")

    async with websockets.serve(
        websocket_handler,
        "0.0.0.0",
        8765,
    ):
        await asyncio.Future()
