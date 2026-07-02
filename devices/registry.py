# Simple in-memory device registry

devices = {}

def register_device(device_id, websocket, metadata=None):
    devices[device_id] = {
        "ws": websocket,
        "metadata": metadata or {}
    }
    print(f"[Registry] Registered device: {device_id}")


def unregister_device(device_id):
    if device_id in devices:
        del devices[device_id]
        print(f"[Registry] Unregistered device: {device_id}")


def get_device(device_id):
    return devices.get(device_id)


def list_devices():
    return devices


def export_devices():
    return {
        device_id: {
            "metadata": info.get("metadata", {})
        }
        for device_id, info in devices.items()
    }
