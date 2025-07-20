import { HyperdeckTransportMode, type MatchTime, type RealtimeScore } from './model';

export interface ServerState {
    server_connected: boolean;
    arena_connected: boolean;
    hyperdeck_connected: boolean;

    realtime_score?: RealtimeScore;
    match_time?: MatchTime;
    hyperdeck_transport_mode: HyperdeckTransportMode;
}

/** All state reported by the server to websocket clients */
export const server_state: ServerState = $state({
    server_connected: false,
    arena_connected: false,
    hyperdeck_connected: false,

    realtime_score: undefined,
    match_time: undefined,
    hyperdeck_transport_mode: HyperdeckTransportMode.InputPreview,
})