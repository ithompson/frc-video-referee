import asyncio
import enum
import logging
from typing import Awaitable, Callable, Dict, List
import httpx
from pydantic import BaseModel
import websockets

from frc_video_referee.hyperdeck.model import (
    PLACEHOLDER_PLAYBACK_STATE,
    Clip,
    ClipList,
    ClipResponse,
    EventMessage,
    InboundWebsocketMessage,
    PlaybackState,
    PlaybackType,
    RecordRequest,
    RequestMessage,
    ResponseMessage,
    SubscribeRequest,
    SubscribeResponse,
    TimelineClip,
    TimelineClipList,
    TransportMode,
    TransportModeRequest,
)
from frc_video_referee.utils import ExitServer

logger = logging.getLogger(__name__)


class HyperdeckClientSettings(BaseModel):
    address: str = "localhost:8001"


class HyperdeckNotifier(enum.Enum):
    """Notifiers that can be subscribed by the rest of the system"""

    CONNECTION_STATE_UPDATED = enum.auto()
    """Connection state to the HyperDeck has changed"""
    TRANSPORT_MODE_UPDATED = enum.auto()
    """Transport mode of the HyperDeck has changed"""
    PLAYBACK_STATE_UPDATED = enum.auto()
    """Playback state of the HyperDeck has changed"""
    CLIP_LIST_UPDATED = enum.auto()
    """The list of playable clips on the HyperDeck has updated"""


class HyperdeckClient:
    def __init__(self, settings: HyperdeckClientSettings):
        self._settings = settings
        self._clips: Dict[int, Clip] = {}
        """Dictionary mapping clip IDs to Clip objects"""
        self._timeline: Dict[int, TimelineClip] = {}
        """Dictionary mapping clip IDs to their timeline representation"""
        self._connected = False
        """Whether the client is currently connected to the HyperDeck"""

        self.playback_state = PLACEHOLDER_PLAYBACK_STATE
        """Current playback state"""
        self.transport_mode = TransportMode.InputPreview
        """Current transport mode"""

        self._subscribers: Dict[
            HyperdeckNotifier, List[Callable[[], Awaitable[None]]]
        ] = {notifier: [] for notifier in HyperdeckNotifier}
        """Subscribers for various arena state changes"""

    def subscribe(
        self, notifier: HyperdeckNotifier, callback: Callable[[], Awaitable[None]]
    ):
        """Subscribe to a specific HyperDeck state change."""
        self._subscribers[notifier].append(callback)

    @property
    def connected(self) -> bool:
        """True if the client is connected to the HyperDeck, False otherwise"""
        return self._connected

    @property
    def recording(self) -> bool:
        """True if a recording is currently in progress, False otherwise"""
        return self.transport_mode == TransportMode.InputRecord

    def has_playable_clip(self, clip_id: int) -> bool:
        """Check if a clip with the given ID exists in the HyperDeck and is available for playback."""
        return clip_id in self._clips and clip_id in self._timeline

    def get_clip(self, clip_id: int) -> Clip | None:
        """Get a Clip object by its ID."""
        return self._clips.get(clip_id)

    async def run(self) -> None:
        """Run the Hyperdeck client."""
        async with httpx.AsyncClient(
            base_url=f"http://{self._settings.address}/control/api/v1"
        ) as client:
            logger.info("Starting Hyperdeck client")
            self._client = client

            while True:
                try:
                    await self._run_internal(client)
                except ExitServer:
                    raise
                except httpx.RequestError as e:
                    logger.exception(f"HTTP request error: {e}")
                except Exception as e:
                    logger.exception(f"Internal Hyperdeck client error: {e}")
                logger.info("Reconnecting in 3 seconds...")
                await asyncio.sleep(3)

    async def _run_internal(self, client: httpx.AsyncClient) -> None:
        async with websockets.connect(
            f"ws://{self._settings.address}/control/api/v1/events/websocket"
        ) as websocket:
            logger.info("HyperDeck connection established")
            self._connected = True

            try:
                await self._get_full_clip_list(client)

                subscribe_msg = RequestMessage(
                    data=SubscribeRequest(
                        properties=[
                            "/transports/0/playback",
                            "/transports/0",
                            "/timelines/0",
                        ]
                    )
                )
                await websocket.send(subscribe_msg.model_dump_json(exclude_none=True))

                while True:
                    message_bytes = await websocket.recv(decode=False)
                    message = InboundWebsocketMessage.validate_json(message_bytes)

                    match message:
                        case ResponseMessage():
                            if isinstance(message.data, SubscribeResponse):
                                if message.data.success:
                                    logger.info(
                                        f"Subscribed to properties: {message.data.properties}"
                                    )
                                    for prop, value in message.data.values.items():
                                        await self._handle_property_change(prop, value)
                                else:
                                    raise RuntimeError("HyperDeck subscription failed")
                        case EventMessage():
                            logger.info(
                                f"Received event: {message.data.property} = {message.data.value}"
                            )
                            await self._handle_property_change(
                                message.data.property, message.data.value
                            )
            finally:
                self._connected = False
                logger.info("HyperDeck connection closed")

    async def _handle_property_change(self, property: str, value: dict) -> None:
        """Handle property changes received from the HyperDeck WebSocket."""
        match property:
            case "/transports/0/playback":
                self.playback_state = PlaybackState.model_validate(value)
                await self._notify(HyperdeckNotifier.PLAYBACK_STATE_UPDATED)
            case "/transports/0":
                mode = TransportModeRequest.model_validate(value)
                self.transport_mode = mode.mode
                await self._notify(HyperdeckNotifier.TRANSPORT_MODE_UPDATED)
            case "/timelines/0":
                # Update our view of the timeline structure
                timeline = TimelineClipList.model_validate(value)
                old_timeline_keys = set(self._timeline.keys())
                self._timeline = {clip.clipUniqueId: clip for clip in timeline.clips}
                new_timeline_keys = set(self._timeline.keys())
                if old_timeline_keys != new_timeline_keys:
                    await self._notify(HyperdeckNotifier.CLIP_LIST_UPDATED)

    async def _get_full_clip_list(self, client: httpx.AsyncClient) -> None:
        """Fetch the full list of clips from the HyperDeck."""
        response = await client.get("/clips")
        response.raise_for_status()
        clip_list = ClipList.model_validate_json(response.text)
        logger.info(f"Retrieved {len(clip_list.clips)} clips from HyperDeck")

        old_clip_keys = set(self._clips.keys())
        self._clips = {clip.clipUniqueId: clip for clip in clip_list.clips}
        new_clip_keys = set(self._clips.keys())

        if old_clip_keys != new_clip_keys:
            await self._notify(HyperdeckNotifier.CLIP_LIST_UPDATED)

    async def start_recording(self, clip_name: str | None = None) -> int:
        """Start recording a new clip and return the ID in the HyperDeck"""
        request = RecordRequest(clipName=clip_name)
        response = await self._client.post(
            "/transports/0/record",
            content=request.model_dump_json(exclude_none=True),
        )
        response.raise_for_status()

        # Retrieve the new clip's metadata
        response = await self._client.get("/transports/0/clip")
        response.raise_for_status()
        clip_data = ClipResponse.model_validate_json(response.text)
        assert clip_data.clip is not None, "Clip data should not be None"
        self._clips[clip_data.clip.clipUniqueId] = clip_data.clip
        await self._notify(HyperdeckNotifier.CLIP_LIST_UPDATED)

        logger.info(
            f"Started recording clip: {clip_name} with ID {clip_data.clip.clipUniqueId}"
        )
        return clip_data.clip.clipUniqueId

    async def stop_recording(self) -> None:
        """Stop the current recording."""
        response = await self._client.post("/transports/0/stop")
        response.raise_for_status()
        logger.info("Stopped recording")

        # Refresh the clip's metadata now that the recording has stopped
        response = await self._client.get("/transports/0/clip")
        response.raise_for_status()
        clip_data = ClipResponse.model_validate_json(response.text)
        assert clip_data.clip is not None, "Clip data should not be None"
        self._clips[clip_data.clip.clipUniqueId] = clip_data.clip

    def _get_timeline_position(self, clip_id: int, time_frames: int) -> int:
        """Get the timeline position for a specific clip and time frame."""
        try:
            timeline_clip = self._timeline[clip_id]
        except KeyError:
            logger.error(
                f"Attempted to get timeline position for unknown clip ID {clip_id}. Warping to start of timeline"
            )
            return 0

        frame_in_clip = time_frames
        frame_in_clip = max(
            timeline_clip.clipIn, frame_in_clip
        )  # Ensure we don't go before the clip's start
        frame_in_clip = min(
            frame_in_clip, timeline_clip.clipIn + timeline_clip.frameCount - 1
        )  # Ensure we don't go past the clip's end

        return timeline_clip.timelineIn + frame_in_clip - timeline_clip.clipIn

    async def warp_to_clip(self, clip_id: int, time_sec: float) -> None:
        """Warp to a specific clip by its ID and timestamp within the clip."""
        try:
            clip = self._clips[clip_id]
        except KeyError:
            raise ValueError(f"Clip ID '{clip_id}' not found in HyperDeck") from None

        time_frames = int(time_sec * clip.videoFormat.frameRate)

        timeline_position = self._get_timeline_position(clip_id, time_frames)
        request = PlaybackState(
            type=PlaybackType.Jog,
            loop=False,
            singleClip=True,
            speed=1.0,
            position=timeline_position,
        )
        response = await self._client.put(
            "/transports/0/playback", content=request.model_dump_json()
        )
        response.raise_for_status()

    async def show_live_view(self) -> None:
        """Show the live view from the HyperDeck."""
        request = TransportModeRequest(mode=TransportMode.InputPreview)
        response = await self._client.put(
            "/transports/0", content=request.model_dump_json()
        )
        response.raise_for_status()

    async def _notify(self, notifier: HyperdeckNotifier):
        """Notify subscribers of a state change."""
        for callback in self._subscribers[notifier]:
            try:
                await callback()
            except Exception as e:
                logger.error(f"Error notifying subscriber for {notifier.name}: {e}")
