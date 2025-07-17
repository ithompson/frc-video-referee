import asyncio
import logging

from pydantic import BaseModel
from frc_video_referee.hyperdeck.client import HyperdeckClient
from frc_video_referee.cheesy_arena.client import ArenaNotifier, CheesyArenaClient

logger = logging.getLogger(__name__)


class VARSettings(BaseModel):
    pass


class VARController:
    def __init__(
        self,
        settings: VARSettings,
        arena: CheesyArenaClient,
        hyperdeck: HyperdeckClient,
    ):
        self._settings = settings
        self._arena = arena
        self._hyperdeck = hyperdeck

        self._arena.subscribe(ArenaNotifier.MATCH_STARTED, self._handle_match_start)
        self._arena.subscribe(ArenaNotifier.MATCH_ENDED, self._handle_match_end)

    async def run(self):
        while True:
            await asyncio.sleep(
                999
            )  # Placeholder for if an actual controller loop is needed

    async def _handle_match_start(self):
        clip_id = await self._hyperdeck.start_recording()
        logger.info(f"Match started, recording clip ID: {clip_id}")

    async def _handle_match_end(self):
        async def delayed_stop():
            await asyncio.sleep(5)
            await self._hyperdeck.stop_recording()
            logger.info("Recording stopped after scoring period")

        asyncio.create_task(delayed_stop())
