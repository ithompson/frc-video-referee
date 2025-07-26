import { HyperdeckTransportMode, MatchState, MatchStatus, MatchType, PLACEHOLDER_REALTIME_SCORE, type ControllerStatus, type HyperdeckStatus, type Match, type MatchTime, type RealtimeScore } from './model';

export interface ServerState {
    arena_connected: boolean;
    hyperdeck_connected: boolean;
    controller_status: ControllerStatus;

    current_match: Match;
    realtime_score: RealtimeScore;
    match_time: MatchTime;
    hyperdeck_status: HyperdeckStatus;
}

/** All state reported by the server to websocket clients */
export const server_state: ServerState = $state({
    arena_connected: false,
    hyperdeck_connected: false,
    controller_status: {
        selected_match_id: null,
        recording: false,
        realtime_data: true,
    },

    current_match: {
        id: 0,
        match_type: MatchType.TEST,
        type_order: 0,
        long_name: '',
        short_name: '',
        red1: 0,
        red2: 0,
        red3: 0,
        blue1: 0,
        blue2: 0,
        blue3: 0,
        status: MatchStatus.SCHEDULED,
    },
    realtime_score: PLACEHOLDER_REALTIME_SCORE,
    match_time: {
        match_state: MatchState.PRE_MATCH,
        match_time_sec: 0,
    },
    hyperdeck_status: {
        transport_mode: HyperdeckTransportMode.InputPreview,
        playing: false,
        clip_time: 0,
    },
})