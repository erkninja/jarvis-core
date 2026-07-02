import json

from devices.registry import (
    register_device,
    unregister_device,
    export_devices,
)

from audio.receiver import receive_audio


# --------------------------------------------------
# WebSocket Message Handler
# --------------------------------------------------
async def websocket_handler(websocket):

    device_id = None

    print("[WebSocket] New connection")

    try:
        async for message in websocket:

            # ==================================================
            # BINARY AUDIO STREAM
            # ==================================================
            if isinstance(message, bytes):

                if device_id is None:
                    continue

                receive_audio(device_id, message)
                continue

            # ==================================================
            # JSON MESSAGE
            # ==================================================
            try:
                data = json.loads(message)
            except Exception:
                print("[WebSocket] Invalid JSON ignored")
                continue

            msg_type = data.get("type")

            # --------------------------------------------------
            # REGISTER DEVICE
            # --------------------------------------------------
            if msg_type == "register":

                device_id = data.get("device_id", "unknown")

                register_device(
                    device_id=device_id,
                    websocket=websocket,
                    metadata=data.get("metadata", {}),
                )

                print(f"[Registry] Registered device: {device_id}")

                await websocket.send(json.dumps({
                    "type": "registered",
                    "device_id": device_id
                }))

            # --------------------------------------------------
            # LIST DEVICES
            # --------------------------------------------------
            elif msg_type == "list_devices":

                await websocket.send(json.dumps({
                    "type": "devices",
                    "devices": export_devices(),
                }))

            # --------------------------------------------------
            # UNKNOWN MESSAGE
            # --------------------------------------------------
            else:
                print(f"[WebSocket] Unknown message type: {msg_type}")

    except Exception as e:
        print(f"[WebSocket] Connection error: {e}")

    finally:
        if device_id:
            unregister_device(device_id)
            print(f"[Registry] Unregistered device: {device_id}")
