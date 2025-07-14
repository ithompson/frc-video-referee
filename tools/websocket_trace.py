# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "websockets",
# ]
# ///
"""
Test script to monitor WebSocket messages sent by a HyperDeck server.
"""

import asyncio
import json
import pprint
import websockets


async def main():
    ws_url = "ws://localhost:8001/control/api/v1/events/websocket"

    async with websockets.connect(ws_url) as websocket:
        subscribe_msg = {
            "data": {
                "action": "subscribe",
                "properties": [
                    "/transports/0/playback",
                    "/transports/0/record",
                    "/transports/0/clipIndex",
                    "/transports/0",
                    "/timelines/0",
                ],
            },
            "type": "request",
            "id": 1,
        }
        await websocket.send(json.dumps(subscribe_msg))
        print("Sent subscription request")

        while True:
            message = await websocket.recv()
            msg_dict = json.loads(message)
            pprint.pp(msg_dict)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
