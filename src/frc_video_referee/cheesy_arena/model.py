"""
This module defines the data types for the Cheesy Arena APIs used in this application.
"""

from enum import IntEnum
from pydantic import BaseModel, Field, TypeAdapter
from typing import Annotated, Any, List, Dict

###################################
# Baseline Data Types
###################################


class BaseArenaModel(BaseModel, validate_by_name=True):
    pass


class MatchType(IntEnum):
    """Types of matches in the arena"""

    TEST = 0
    PRACTICE = 1
    QUALIFICATION = 2
    PLAYOFF = 3


class MatchStatus(IntEnum):
    """Play status of a match"""

    SCHEDULED = 0
    """Match is scheduled but not played yet"""
    HIDDEN = 1
    """Match is hidden from the schedule, e.g. a skipped playoff match"""
    RED_WON = 2
    """Match was played and the Red alliance won"""
    BLUE_WON = 3
    """Match was played and the Blue alliance won"""
    TIE = 4
    """Match was played and ended in a tie"""


class Match(BaseArenaModel):
    """Schedule data for a match"""

    id: Annotated[int, Field(alias="Id")]
    """Internal arena ID for the match"""
    match_type: Annotated[MatchType, Field(alias="Type")]
    """Type of the match, e.g., qualification, playoff, etc."""
    type_order: Annotated[int, Field(alias="TypeOrder")]
    """Order of the match within its type"""
    long_name: Annotated[str, Field(alias="LongName")]
    """Full name of the match, e.g., "Qualification Match 1"."""
    short_name: Annotated[str, Field(alias="ShortName")]
    """Abbreviated name of the match, e.g., "Q1"."""

    red1: Annotated[int, Field(alias="Red1")]
    """Team number in the Red 1 station"""
    red2: Annotated[int, Field(alias="Red2")]
    """Team number in the Red 2 station"""
    red3: Annotated[int, Field(alias="Red3")]
    """Team number in the Red 3 station"""
    blue1: Annotated[int, Field(alias="Blue1")]
    """Team number in the Blue 1 station"""
    blue2: Annotated[int, Field(alias="Blue2")]
    """Team number in the Blue 2 station"""
    blue3: Annotated[int, Field(alias="Blue3")]
    """Team number in the Blue 3 station"""

    status: Annotated[MatchStatus, Field(alias="Status")]
    """Overall status of the match, whether it was played and which alliance won."""


class Team(BaseArenaModel):
    """Represents a team in the event."""

    team_num: Annotated[int, Field(alias="Id")]
    """Team number"""


class MatchState(IntEnum):
    """State of a match play cycle"""

    PRE_MATCH = 0
    """Match is loaded but not started yet"""
    START_MATCH = 1
    """Start match has been pressed, arena is transitioning to the match play state"""
    WARMUP_PERIOD = 2
    """Pre-match warmup period is in progress. Not used in most years."""
    AUTO_PERIOD = 3
    """Autonomous period is in progress"""
    PAUSE_PERIOD = 4
    """Period between autonomous and teleop is in progress"""
    TELEOP_PERIOD = 5
    """Teleoperated period is in progress"""
    POST_MATCH = 6
    """Match is ended"""
    TIMEOUT_ACTIVE = 7
    """A timeout is in progress"""
    POST_TIMEOUT = 8
    """A timeout has completed but the next match has not been loaded yet"""


####################################
# Game-specific scoring data types
####################################


ReefRow = Annotated[List[bool], Field(min_length=12, max_length=12)]


class Reef(BaseArenaModel):
    auto_branches: Annotated[
        List[ReefRow], Field(min_length=3, max_length=3, alias="AutoBranches")
    ]
    """Whether coral was placed on each branch during the autonomous period"""
    branches: Annotated[
        List[ReefRow], Field(min_length=3, max_length=3, alias="Branches")
    ]
    """Whether coral is currently placed on each branch"""
    auto_trough_near: Annotated[int, Field(alias="AutoTroughNear")]
    """Number of coral in the L1 trough during the autonomous period, near side counter"""
    auto_trough_far: Annotated[int, Field(alias="AutoTroughFar")]
    """Number of coral in the L1 trough during the autonomous period, far side counter"""
    trough_near: Annotated[int, Field(alias="TroughNear")]
    """Number of coral in the L1 trough, near side counter"""
    trough_far: Annotated[int, Field(alias="TroughFar")]
    """Number of coral in the L1 trough, far side counter"""


PLACEHOLDER_REEF = Reef(
    auto_branches=[[False] * 12] * 3,
    branches=[[False] * 12] * 3,
    auto_trough_near=0,
    auto_trough_far=0,
    trough_near=0,
    trough_far=0,
)


class Foul(BaseArenaModel):
    is_major: Annotated[bool, Field(alias="IsMajor")]
    """Whether this is a major or minor foul"""
    team_id: Annotated[int, Field(alias="TeamId")]
    """The team that committed the foul"""
    rule_id: Annotated[int, Field(alias="RuleId")]
    """The rule that was violated"""


class EndgameStatus(IntEnum):
    """Endgame points qualification status"""

    NONE = 0
    """No endgame points"""
    PARKED = 1
    """Qualified for park points"""
    SHALLOW_CAGE = 2
    """Qualified for shallow cage points"""
    DEEP_CAGE = 3
    """Qualified for deep cage points"""


class Score(BaseArenaModel):
    """Represents an alliance's score components in a match."""

    leave_statuses: Annotated[
        List[bool], Field(min_length=3, max_length=3, alias="LeaveStatuses")
    ]
    """Whether each team qualified for leave points"""
    reef: Annotated[Reef, Field(alias="Reef")]
    """Reef scoring data"""
    barge_algae: Annotated[int, Field(alias="BargeAlgae")]
    """Number of algae placed on the barge"""
    processor_algae: Annotated[int, Field(alias="ProcessorAlgae")]
    """Number of algae placed in the processor"""
    endgame_statuses: Annotated[
        List[EndgameStatus], Field(min_length=3, max_length=3, alias="EndgameStatuses")
    ]
    """Endgame statuses for each team"""
    fouls: Annotated[List[Foul] | None, Field(alias="Fouls")]
    """List of fouls committed by the alliance, or None if no fouls were committed"""


PLACEHOLDER_SCORE = Score(
    leave_statuses=[False, False, False],
    reef=PLACEHOLDER_REEF,
    barge_algae=0,
    processor_algae=0,
    endgame_statuses=[EndgameStatus.NONE] * 3,
    fouls=None,
)


class ScoreSummary(BaseArenaModel):
    """Final score tallies for an alliance in a match."""

    match_points: Annotated[int, Field(alias="MatchPoints")]
    """Total points scored by the alliance in the match"""


PLACEHOLDER_SCORE_SUMMARY = ScoreSummary(match_points=0)


#############################################
# Match results HTTP endpoint response types
#############################################


class MatchResult(BaseArenaModel):
    """The baseline results of a match which are stored in the arena database."""

    match_id: Annotated[int, Field(alias="MatchId")]
    """Internal arena ID for the match"""
    play_number: Annotated[int, Field(alias="PlayNumber")]
    """How many times this match has been played, 1 for the first play, 2 for a replay, etc."""
    match_type: Annotated[MatchType, Field(alias="MatchType")]
    """Type of the match, e.g., qualification, playoff, etc."""
    red_score: Annotated[Score, Field(alias="RedScore")]
    """Score data for the Red alliance"""
    blue_score: Annotated[Score, Field(alias="BlueScore")]
    """Score data for the Blue alliance"""
    red_cards: Annotated[Dict[int, str], Field(alias="RedCards")]
    """Red alliance cards issued during the match, keyed by team number"""
    blue_cards: Annotated[Dict[int, str], Field(alias="BlueCards")]
    """Blue alliance cards issued during the match, keyed by team number"""


class MatchResultWithSummary(MatchResult):
    """Match results with final scores computed"""

    red_summary: Annotated[ScoreSummary, Field(alias="RedSummary")]
    """Final score summary for the Red alliance"""
    blue_summary: Annotated[ScoreSummary, Field(alias="BlueSummary")]
    """Final score summary for the Blue alliance"""


class MatchWithResultAndSummary(Match):
    """Match schedule information with its results"""

    result: Annotated[MatchResultWithSummary, Field(alias="Result")]
    """Results of the match, including final scores"""


MatchResultList = TypeAdapter(List[MatchWithResultAndSummary])
"""List of match results"""


###########################
# Websocket message types #
###########################


class MatchLoadMessage(BaseArenaModel):
    """Contents of a matchLoad message"""

    match_info: Annotated[Match, Field(alias="Match")]
    """Information about the match being loaded"""
    is_replay: Annotated[bool, Field(alias="IsReplay")]
    """Whether this is a replay of a match"""
    teams: Annotated[Dict[str, Team | None], Field(alias="Teams")]
    """Teams participating in the match, keyed by station ID as a string"""


PLACEHOLDER_MATCH_LOAD_MESSAGE = MatchLoadMessage(
    match_info=Match(
        id=0,
        match_type=MatchType.TEST,
        type_order=0,
        long_name="Test Match",
        short_name="T",
        red1=0,
        red2=0,
        red3=0,
        blue1=0,
        blue2=0,
        blue3=0,
        status=MatchStatus.SCHEDULED,
    ),
    is_replay=False,
    teams={},
)


class MatchTimeMessage(BaseArenaModel):
    """Contents of a matchTime message"""

    match_state: Annotated[MatchState, Field(alias="MatchState")]
    """Current state of the match play cycle"""
    match_time_sec: Annotated[int, Field(alias="MatchTimeSec")]
    """Current match time in seconds, 0 for pre- or post-match state"""


PLACEHOLDER_MATCH_TIME_MESSAGE = MatchTimeMessage(
    match_state=MatchState.PRE_MATCH, match_time_sec=0
)


class ScoreWithSummary(BaseArenaModel):
    """Represents an alliance's score with a summary."""

    score: Annotated[Score, Field(alias="Score")]
    """Raw scoring data for the alliance"""
    score_summary: Annotated[ScoreSummary, Field(alias="ScoreSummary")]
    """Final score summary for the alliance"""


PLACEHOLDER_SCORE_WITH_SUMMARY = ScoreWithSummary(
    score=PLACEHOLDER_SCORE, score_summary=PLACEHOLDER_SCORE_SUMMARY
)


class RealtimeScoreMessage(BaseArenaModel):
    """Contents of a realtimeScore message"""

    red: Annotated[ScoreWithSummary, Field(alias="Red")]
    """Score data for the Red alliance"""
    blue: Annotated[ScoreWithSummary, Field(alias="Blue")]
    """Score data for the Blue alliance"""
    red_cards: Annotated[Dict[int, str], Field(alias="RedCards")]
    """Red alliance cards issued during the match, keyed by team number"""
    blue_cards: Annotated[Dict[int, str], Field(alias="BlueCards")]
    """Blue alliance cards issued during the match, keyed by team number"""


PLACEHOLDER_REALTIME_SCORE_MESSAGE = RealtimeScoreMessage(
    red=PLACEHOLDER_SCORE_WITH_SUMMARY,
    blue=PLACEHOLDER_SCORE_WITH_SUMMARY,
    red_cards={},
    blue_cards={},
)


class PositionStatus(BaseArenaModel):
    """Status for a referee and scorer position"""

    num_panels: Annotated[int, Field(alias="NumPanels")]
    """How many panels are connected to the arena for this position"""
    num_panels_ready: Annotated[int, Field(alias="NumPanelsReady")]
    """How many panels are signaling scores ready for this position"""
    ready: Annotated[bool, Field(alias="Ready")]
    """Whether this position has completd scoring"""


class ScoringStatusMessage(BaseArenaModel):
    """Contents of a scoringStatus message"""

    referee_score_ready: Annotated[bool, Field(alias="RefereeScoreReady")]
    """Whether the head referee has completed scoring"""
    position_statuses: Annotated[
        Dict[str, PositionStatus], Field(alias="PositionStatuses")
    ]
    """Status of each scoring position, keyed by position name"""


class ArenaStatusMessage(BaseArenaModel):
    """Contents of an arenaStatus message"""

    can_start_match: Annotated[bool, Field(alias="CanStartMatch")]
    """Whether the arena is ready to start a match"""


PLACEHOLDER_ARENA_STATUS_MESSAGE = ArenaStatusMessage(can_start_match=False)


class WebsocketMessage(BaseArenaModel):
    """Base type for inbound websocket messages."""

    type: str
    data: Any
