/* Game-specific score model */

export type ReefRow = [boolean, boolean, boolean, boolean, boolean, boolean, boolean, boolean, boolean, boolean, boolean, boolean];
export type ReefBranches = [ReefRow, ReefRow, ReefRow]

export interface Reef {
    auto_branches: ReefBranches;
    branches: ReefBranches;
    auto_trough_near: number;
    auto_trough_far: number;
    trough_near: number;
    trough_far: number;
}

export interface Foul {
    is_major: boolean;
    team_id: number;
    rule_id: number;
}

export enum EndgameStatus {
    NONE = 0,
    PARKED = 1,
    SHALLOW_CAGE = 2,
    DEEP_CAGE = 3,
}

export interface Score {
    leave_statuses: [boolean, boolean, boolean];
    reef: Reef;
    barge_algae: number;
    processor_algae: number;
    endgame_statuses: [EndgameStatus, EndgameStatus, EndgameStatus];
}

export interface ScoreSummary {
    match_points: number
}

export interface ScoreWithSummary {
    score: Score;
    score_summary: ScoreSummary;
}

export interface Cards {
    [index: number]: string;
}

export interface RealtimeScore {
    red: ScoreWithSummary;
    blue: ScoreWithSummary;
    red_cards: Cards;
    blue_cards: Cards;
}

/* Evergreen arena status */

export enum MatchState {
    PRE_MATCH = 0,
    START_MATCH = 1,
    WARMUP_PERIOD = 2,
    AUTO_PERIOD = 3,
    PAUSE_PERIOD = 4,
    TELEOP_PERIOD = 5,
    POST_MATCH = 6,
    TIMEOUT_ACTIVE = 7,
    POST_TIMEOUT = 8,
}

export interface MatchTime {
    match_state: MatchState;
    match_time_sec: number;
}

export enum MatchType {
    TEST = 0,
    PRACTICE = 1,
    QUALIFICATION = 2,
    PLAYOFF = 3,
}

/** Play status of a match */
export enum MatchStatus {
    /** Match is scheduled but not played yet*/
    SCHEDULED = 0,
    /** Match is hidden from the schedule, e.g. a skipped playoff match */
    HIDDEN = 1,
    /** Match was played and the Red alliance won */
    RED_WON = 2,
    /** Match was played and the Blue alliance won */
    BLUE_WON = 3,
    /** Match was played and ended in a tie */
    TIE = 4,
}

/** Schedule data for a match */
export interface Match {
    /** Internal arena ID for the match */
    id: number;
    /** Type of the match, eg qualification or playoff */
    match_type: MatchType;
    /** Order of the match within its type */
    type_order: number;
    /** Full name for the match */
    long_name: string;
    /** Abbreviated name for the match */
    short_name: string;
    /** Team number in the Red 1 station */
    red1: number;
    /** Team number in the Red 2 station */
    red2: number;
    /** Team number in the Red 3 station */
    red3: number;
    /** Team number in the Blue 1 station */
    blue1: number;
    /** Team number in the Blue 2 station */
    blue2: number;
    /** Team number in the Blue 3 station */
    blue3: number;
    /** Overall status of the match, whether it was played and which alliance won. */
    status: MatchStatus;
}

export interface MatchResult {
    /** Internal arena ID for the match */
    match_id: number;
    /** How many times this match has been played, 1 for the first place, 2 for a replay, etc. */
    play_number: number;
    /** Type of the match */
    match_type: MatchType;
    /** Score data for the red alliance */
    red_score: Score;
    /** Score data for the blue alliance */
    blue_score: Score;
    /** Red alliance cards issued during the match */
    red_cards: Cards;
    /** Blue alliance cards issued during the match */
    blue_cards: Cards;
}

export interface MatchResultWithSummary extends MatchResult {
    /** Summary of the red match score */
    red_summary: ScoreSummary;
    /** Summary of the blue match score */
    blue_summary: ScoreSummary;
}

export interface MatchWithResultAndSummary extends Match {
    /** Results of the match, including final scores */
    result: MatchResultWithSummary;
}

/* Hyperdeck status types */
export enum HyperdeckTransportMode {
    InputPreview = "InputPreview",
    InputRecord = "InputRecord",
    Output = "Output",
}

export enum HyperdeckPlaybackType {
    Play = "Play",
    Jog = "Jog",
    Shuttle = "Shuttle",
    Var = "Var",
}

export interface HyperdeckPlaybackState {
    type: HyperdeckPlaybackType;
    loop: boolean;
    singleClip: boolean;
    speed: number;
    position: number;
}

export enum WebsocketEventType {
    CurrentMatchData = "current_match_data",
    CurrentMatchTime = "current_match_time",
    RealtimeScore = "realtime_score",
    MatchList = "match_list",
    ArenaConnection = "arena_connection",
    HyperdeckConnection = "hyperdeck_connection",
    HyperdeckTransportMode = "hyperdeck_transport_mode",
    HyperdeckPlaybackState = "hyperdeck_playback_state",
}

export interface WebsocketEvent {
    type: 'event';
    event_type: string;
    data: any;
}

export interface WebsocketSubscribeResponse {
    type: 'subscribe';
    initial_data: Partial<Record<string, any>>;
}