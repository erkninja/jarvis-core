import asyncio

from websocket.server import start_server


def main():
    print("[Jarvis] Booting...")

    asyncio.run(start_server())


if __name__ == "__main__":
    main()
