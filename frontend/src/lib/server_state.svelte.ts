import { HyperdeckTransportMode, MatchState, PLACEHOLDER_REALTIME_SCORE, type ControllerStatus, type HyperdeckStatus, type MatchTime, type RealtimeScore } from './model';

export interface ServerState {
    arena_connected: boolean;
    hyperdeck_connected: boolean;
    controller_status: ControllerStatus;

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