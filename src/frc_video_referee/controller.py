import asyncio
import enum
import logging
from datetime import datetime

from pydantic import BaseModel
from frc_video_referee import db
from frc_video_referee.db.model import MatchEvent, MatchEventType, RecordedMatch
from frc_video_referee.hyperdeck.client import HyperdeckClient, HyperdeckNotifier
from frc_video_referee.cheesy_arena.client import ArenaNotifier, CheesyArenaClient
from frc_video_referee.web import WebsocketManager

logger = logging.getLogger(__name__)

# Event names used on the websocket interface
CURRENT_MATCH_DATA_EVENT = "current_match_data"
CURRENT_MATCH_TIME_EVENT = "current_match_time"
REALTIME_SCORE_EVENT = "realtime_score"
MATCH_LIST_EVENT = "match_list"
ARENA_CONNECTION_EVENT = "arena_connection"
HYPERDECK_CONNECTION_EVENT = "hyperdeck_connection"
HYPERDECK_TRANSPORT_MODE_EVENT = "hyperdeck_transport_mode"
HYPERDECK_PLAYBACK_EVENT = "hyperdeck_playback"


class VARSettings(BaseModel):
    """Settings for the VAR controller"""

    auto_scoring_delay: float = 3.0
    """Delay in seconds after AUTO ends before scoring is evaluated"""

    endgame_scoring_delay: float = 3.0
    """Delay in seconds after the match ends before scoring is evaluated"""

    recording_extra_time: float = 2.0
    """Extra time in seconds after endgame scoring to keep the recording running"""


class ControllerState(enum.Enum):
    Idle = enum.auto()
    """No recording or playback in progress, showing live camera feed"""
    Recording = enum.auto()
    """Currently recording a match"""
    ReviewingCurrentMatch = enum.auto()
    """Reviewing the current match that was just recorded but has not been committed"""
    ReviewingHistoricalMatch = enum.auto()
    """Reviewing a historical match that was previously recorded and committed"""


class VARController:
    """Main controller and business logic for the Video Assistant Referee (VAR) system"""

    def __init__(
        self,
        settings: VARSettings,
        arena: CheesyArenaClient,
        hyperdeck: HyperdeckClient,
        websocket: WebsocketManager,
        db: db.DB,
    ):
        self._settings = settings
        self._arena = arena
        self._hyperdeck = hyperdeck
        self._websocket = websocket
        self._db = db

        self._lock = asyncio.Lock()
        self._state = ControllerState.Idle
        self._matches = self._db.load_all_matches()
        self._current_match: RecordedMatch | None = None

        # Register callbacks for events that the controller is interested in
        arena_subscriptions = [
            # Match lifecycle events
            (ArenaNotifier.ARENA_READY_TO_START, self._handle_arena_ready_to_start),
            (ArenaNotifier.MATCH_STARTED, self._handle_match_start),
            (ArenaNotifier.AUTO_PERIOD_ENDED, self._handle_auto_period_end),
            (ArenaNotifier.MATCH_ENDED, self._handle_match_end),
            (ArenaNotifier.MATCH_COMMITTED_OR_DISCARDED, self._handle_match_commit),
            # UI data update notifications
            (
                ArenaNotifier.CONNECTION_STATE_UPDATED,
                self._handle_arena_connection_state_update,
            ),
            (
                ArenaNotifier.HISTORICAL_SCORES_UPDATED,
                self._handle_historical_scores_update,
            ),
            (
                ArenaNotifier.REALTIME_SCORE_UPDATED,
                self._handle_realtime_score_update,
            ),
            (
                ArenaNotifier.MATCH_TIME_UPDATED,
                self._handle_match_time_update,
            ),
            (
                ArenaNotifier.MATCH_DATA_UPDATED,
                self._handle_match_data_update,
            ),
        ]
        for event, handler in arena_subscriptions:
            self._arena.subscribe(event, handler)

        hyperdeck_subscriptions = [
            # UI data update notifications
            (
                HyperdeckNotifier.CONNECTION_STATE_UPDATED,
                self._handle_hyperdeck_connection_state_update,
            ),
            (
                HyperdeckNotifier.TRANSPORT_MODE_UPDATED,
                self._handle_hyperdeck_transport_mode_update,
            ),
            (
                HyperdeckNotifier.PLAYBACK_STATE_UPDATED,
                self._handle_hyperdeck_playback_state_update,
            ),
            (
                HyperdeckNotifier.CLIP_LIST_UPDATED,
                self._handle_hyperdeck_clip_list_update,
            ),
        ]
        for event, handler in hyperdeck_subscriptions:
            self._hyperdeck.subscribe(event, handler)

        self._websocket.add_event_type(
            CURRENT_MATCH_TIME_EVENT,
            lambda: self._arena.match_time.model_dump(),
        )
        self._websocket.add_event_type(
            REALTIME_SCORE_EVENT,
            lambda: self._arena.realtime_score.model_dump(),
        )
        self._websocket.add_event_type(
            ARENA_CONNECTION_EVENT, lambda: {"connected": self._arena.connected}
        )
        self._websocket.add_event_type(
            HYPERDECK_CONNECTION_EVENT, lambda: {"connected": self._hyperdeck.connected}
        )
        self._websocket.add_event_type(
            HYPERDECK_TRANSPORT_MODE_EVENT,
            lambda: {"transport_mode": self._hyperdeck.transport_mode.name},
        )
        self._websocket.add_event_type(
            HYPERDECK_PLAYBACK_EVENT,
            lambda: self._hyperdeck.playback_state.model_dump(),
        )

    #########################################
    # Helpers for managing controller state #
    #########################################

    def _set_state(self, state: ControllerState):
        """Set the current state of the controller."""
        if self._state == state:
            return
        logger.info(f"Controller state change from {self._state.name} to {state.name}")
        self._state = state

    def _create_id_for_current_match(self) -> str:
        """Generate an ID for the current match based on arena data."""
        arena_match = self._arena.match_data
        match_base_name = arena_match.match_info.short_name
        if arena_match.is_replay:
            match_base_name += "_replay"

        match_id = match_base_name
        match_seqnum = 0
        while match_id in self._matches:
            match_seqnum += 1
            match_id = f"{match_base_name}_{match_seqnum}"

        return match_id

    def _get_current_match_time(self) -> float:
        """Get the current match time in seconds."""
        if self._current_match is None:
            return 0.0
        time_seconds = (
            datetime.now().astimezone() - self._current_match.timestamp
        ).total_seconds()
        return max(0.0, time_seconds)

    async def _save_and_unload_current_match(self):
        """Save the current match to the database and unload it."""
        if self._current_match:
            logger.debug(f"Unloading match {self._current_match.var_id}")
            if self._state == ControllerState.Recording:
                await self._hyperdeck.stop_recording()
                self._set_state(ControllerState.Idle)
            self._matches[self._current_match.var_id] = self._current_match
            self._db.save_match(self._current_match)
            self._current_match = None
            await self._hyperdeck.show_live_view()

    def _add_match_event(self, event: MatchEvent):
        """Add an event to the current match."""
        if self._current_match is None:
            logger.warning("No current match to add event to")
            return

        logger.info(
            f"Match {self._current_match.var_id}: {event.event_type.value} event at {event.time}"
        )

        self._current_match.events.append(event)
        self._db.save_match(self._current_match)

    async def _finalize_match_recording(self):
        """Finalize the current match recording."""
        async with self._lock:
            if self._state != ControllerState.Recording:
                logger.debug("Not in recording state, nothing to finalize")
                return

            assert self._current_match is not None, "No current match to finalize"
            logger.info(f"Match {self._current_match.var_id} ended, stopping recording")

            clip_id = await self._hyperdeck.stop_recording()
            self._current_match.clip_id = clip_id
            self._set_state(ControllerState.ReviewingCurrentMatch)

            auto_end_event = None
            for event in self._current_match.events:
                if event.event_type == MatchEventType.AUTO_SCORING:
                    auto_end_event = event
                    break
            time_to_display = auto_end_event.time if auto_end_event else 0.0
            await self._hyperdeck.warp_to_clip(clip_id, time_to_display)

    #######################################
    # Handlers for match lifecycle events #
    #######################################

    async def _handle_arena_ready_to_start(self):
        """Handle a notification that the arena is now ready for match start"""
        pass

    async def _handle_match_start(self):
        """Handle a notification that a match has started"""
        async with self._lock:
            await self._save_and_unload_current_match()
            self._set_state(ControllerState.Recording)

            match_timestamp = datetime.now().astimezone()
            match_id = self._create_id_for_current_match()
            logger.info(
                f"Starting recording of match {match_id} at {match_timestamp.isoformat()}"
            )

            recording_name = match_id
            clip_id = await self._hyperdeck.start_recording(recording_name)
            logger.debug(f"HyperDeck clip ID: {clip_id} with filename {recording_name}")

            self._current_match = RecordedMatch(
                var_id=match_id,
                arena_id=self._arena.match_data.match_info.id,
                clip_file_name=recording_name,
                timestamp=match_timestamp,
            )
            self._db.save_match(self._current_match)

    async def _handle_auto_period_end(self):
        """Handle a notification that the AUTO period has ended"""
        async with self._lock:
            if self._state != ControllerState.Recording:
                logger.debug("Not in recording state, ignoring auto period end")
                return

            self._add_match_event(
                MatchEvent(
                    event_type=MatchEventType.AUTO_SCORING,
                    time=self._get_current_match_time()
                    + self._settings.auto_scoring_delay,
                )
            )

    async def _handle_match_end(self):
        """Handle a notification that a match has ended"""

        async def delayed_stop():
            """Delay stopping the recording to allow for endgame scoring"""
            await asyncio.sleep(
                self._settings.endgame_scoring_delay
                + self._settings.recording_extra_time
            )
            await self._finalize_match_recording()

        async with self._lock:
            if self._state == ControllerState.Recording:
                self._add_match_event(
                    MatchEvent(
                        event_type=MatchEventType.ENDGAME_SCORING,
                        time=self._get_current_match_time()
                        + self._settings.endgame_scoring_delay,
                    )
                )
                asyncio.create_task(delayed_stop())

    async def _handle_match_commit(self):
        async with self._lock:
            if self._state == ControllerState.ReviewingHistoricalMatch:
                logger.debug("Reviewing a different match, ignoring commit")
                return

            await self._save_and_unload_current_match()
            self._set_state(ControllerState.Idle)

    ###############################################
    # Handlers for arena-related UI data changing #
    ###############################################

    async def _handle_arena_connection_state_update(self):
        """Handle a notification that the arena connection state has changed"""
        await self._websocket.notify(ARENA_CONNECTION_EVENT)

    async def _handle_historical_scores_update(self):
        """Handle a notification that the historical scores have changed"""
        # TODO: propagate update to the UI
        pass

    async def _handle_realtime_score_update(self):
        """Handle a notification that the realtime score has changed"""
        await self._websocket.notify(REALTIME_SCORE_EVENT)

    async def _handle_match_data_update(self):
        """Handle a notification that the match data has changed"""
        # TODO: propagate update to the UI
        pass

    async def _handle_match_time_update(self):
        """Handle a notification that the match time has changed"""
        await self._websocket.notify(CURRENT_MATCH_TIME_EVENT)

    ###################################################
    # Handlers for hyperdeck-related UI data changing #
    ###################################################

    async def _handle_hyperdeck_connection_state_update(self):
        """Handle a notification that the HyperDeck connection state has changed"""
        await self._websocket.notify(HYPERDECK_CONNECTION_EVENT)

    async def _handle_hyperdeck_transport_mode_update(self):
        """Handle a notification that the HyperDeck transport mode has changed"""
        await self._websocket.notify(HYPERDECK_TRANSPORT_MODE_EVENT)

    async def _handle_hyperdeck_playback_state_update(self):
        """Handle a notification that the HyperDeck playback state has changed"""
        await self._websocket.notify(HYPERDECK_PLAYBACK_EVENT)

    async def _handle_hyperdeck_clip_list_update(self):
        """Handle a notification that the HyperDeck clip list has changed"""
        # TODO: propagate update to the UI
        pass
