import { HyperdeckPlaybackType, HyperdeckTransportMode, type HyperdeckPlaybackState, type MatchTime, type RealtimeScore } from './model';

export interface ServerState {
    arena_connected: boolean;
    hyperdeck_connected: boolean;

    realtime_score?: RealtimeScore;
    match_time?: MatchTime;
    hyperdeck_transport_mode: HyperdeckTransportMode;
    hyperdeck_playback_state: HyperdeckPlaybackState;
}

/** All state reported by the server to websocket clients */
export const server_state: ServerState = $state({
    arena_connected: false,
    hyperdeck_connected: false,

    realtime_score: undefined,
    match_time: undefined,
    hyperdeck_transport_mode: HyperdeckTransportMode.InputPreview,
    hyperdeck_playback_state: {
        type: HyperdeckPlaybackType.Jog,
        loop: false,
        singleClip: false,
        speed: 1.0,
        position: 0,
    },
})