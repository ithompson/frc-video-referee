# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "websockets",
# ]
# ///
"""
Test script for the Mock BlackMagic HyperDeck API

This script demonstrates how to interact with the mock HyperDeck API
using both REST endpoints and WebSocket connections.
"""

import asyncio
import json
import requests
import websockets
from typing import Dict, Any


class HyperDeckClient:
    """Simple client for interacting with the mock HyperDeck API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.api_base = f"{base_url}/control/api/v1"
        self.ws_url = "ws://127.0.0.1:8001/control/api/v1/events/websocket"

    def get_status(self) -> Dict[str, Any]:
        """Get server status."""
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json()

    def set_transport_mode(self, mode: str) -> None:
        """Set transport mode."""
        response = requests.put(f"{self.api_base}/transports/0", json={"mode": mode})
        response.raise_for_status()

    def start_recording(self, clip_name: str = None) -> None:
        """Start recording."""
        data = {}
        if clip_name:
            data["clipName"] = clip_name

        response = requests.post(f"{self.api_base}/transports/0/record", json=data)
        response.raise_for_status()

    def stop_recording(self) -> None:
        """Stop recording."""
        response = requests.post(f"{self.api_base}/transports/0/stop")
        response.raise_for_status()

    def get_current_clip(self) -> Dict[str, Any]:
        """Get current clip information."""
        response = requests.get(f"{self.api_base}/transports/0/clip")
        response.raise_for_status()
        return response.json()

    def get_all_clips(self) -> Dict[str, Any]:
        """Get all clips."""
        response = requests.get(f"{self.api_base}/clips")
        response.raise_for_status()
        return response.json()

    def set_playback(
        self, playback_type: str, position: int = 0, speed: float = 1.0
    ) -> None:
        """Set playback configuration."""
        response = requests.put(
            f"{self.api_base}/transports/0/playback",
            json={
                "type": playback_type,
                "loop": False,
                "singleClip": True,
                "speed": speed,
                "position": position,
            },
        )
        response.raise_for_status()

    async def websocket_demo(self) -> None:
        """Demonstrate WebSocket functionality."""
        print("\n=== WebSocket Demo ===")

        try:
            async with websockets.connect(self.ws_url) as websocket:
                print("Connected to WebSocket")

                # Subscribe to some properties
                subscribe_msg = {
                    "data": {
                        "action": "subscribe",
                        "properties": [
                            "/transports/0/record",
                            "/transports/0",
                            "/timelines/0",
                        ],
                    },
                    "type": "request",
                    "id": 1,
                }

                await websocket.send(json.dumps(subscribe_msg))
                print("Sent subscription request")

                # Listen for messages for a few seconds
                try:
                    async with asyncio.timeout(5):
                        while True:
                            message = await websocket.recv()
                            data = json.loads(message)
                            print(
                                f"Received: {data['type']} - {data.get('data', {}).get('action', 'unknown')}"
                            )

                            if data["type"] == "response" and data.get("id") == 1:
                                print("Subscription confirmed")
                                break
                except asyncio.TimeoutError:
                    print("WebSocket demo timeout")

        except Exception as e:
            print(f"WebSocket error: {e}")


async def main():
    """Main test function."""
    client = HyperDeckClient()

    print("=== Mock HyperDeck API Test ===")

    # Test basic status
    print("\n1. Getting server status...")
    status = client.get_status()
    print(f"Status: {status}")

    # Test getting clips
    print("\n2. Getting all clips...")
    clips = client.get_all_clips()
    print(f"Found {len(clips['clips'])} clips")
    for clip in clips["clips"]:
        print(f"  - {clip['filePath']} ({clip['frameCount']} frames)")

    # Test transport mode changes
    print("\n3. Testing transport modes...")
    print("Setting to InputPreview mode...")
    client.set_transport_mode("InputPreview")

    # Test recording
    print("\n4. Testing recording...")
    print("Starting recording...")
    client.start_recording("test_recording.mov")

    print("Waiting 2 seconds...")
    await asyncio.sleep(2)

    print("Getting current clip info...")
    try:
        current_clip = client.get_current_clip()
        print(f"Current clip: {current_clip['clip']['filePath']}")
    except Exception as e:
        print(f"Error getting current clip: {e}")

    print("Stopping recording...")
    client.stop_recording()

    # Test playback
    print("\n5. Testing playback...")
    print("Setting playback to position 250...")
    client.set_playback("Jog", position=250, speed=1.0)

    # Test clips again to see new recording
    print("\n6. Getting updated clips list...")
    clips = client.get_all_clips()
    print(f"Now have {len(clips['clips'])} clips")
    for clip in clips["clips"]:
        print(f"  - {clip['filePath']} ({clip['frameCount']} frames)")

    # WebSocket demo
    await client.websocket_demo()

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    print("Make sure the mock server is running with:")
    print("  python mock_hyperdeck.py")
    print("\nStarting tests in 3 seconds...")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed: {e}")
        print("\nMake sure the mock server is running on http://127.0.0.1:8001")
