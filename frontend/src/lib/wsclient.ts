import { server_state } from './server_state.svelte';
import { HyperdeckTransportMode, WebsocketEventType, type MatchTime, type RealtimeScore } from './model';

function handle_event(type: WebsocketEventType, data: any) {
    switch (type) {
        case WebsocketEventType.CurrentMatchData:
            // Handle match data updates if needed
            console.log('Current match data received:', data);
            break;
        case WebsocketEventType.CurrentMatchTime:
            server_state.match_time = data as MatchTime;
            break;
        case WebsocketEventType.RealtimeScore:
            server_state.realtime_score = data as RealtimeScore;
            break;
        case WebsocketEventType.MatchList:
            // Handle match list updates if needed
            console.log('Match list updated:', data);
            break;
        case WebsocketEventType.ArenaConnection:
            server_state.arena_connected = data.connected;
            break;
        case WebsocketEventType.HyperdeckConnection:
            server_state.hyperdeck_connected = data.connected;
            break;
        case WebsocketEventType.HyperdeckTransportMode:
            server_state.hyperdeck_transport_mode = data.transport_mode as HyperdeckTransportMode;
            break;
        case WebsocketEventType.HyperdeckPlaybackState:
            // Handle hyperdeck playback state updates if needed
            break;
        default:
            console.warn('Unhandled event type:', type);
    }
}

function connect(address: string, subscriptions: WebsocketEventType[] = []) {
    const full_address = `ws://${address}/api/websocket`
    console.log('Connecting to WebSocket at:', full_address)
    const ws = new WebSocket(full_address)

    ws.onopen = () => {
        console.log('WebSocket connection established')
        server_state.server_connected = true
        const subscribe_message = {
            type: 'subscribe',
            event_types: subscriptions,
        };
        ws.send(JSON.stringify(subscribe_message))
    }

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data)
        console.log('WebSocket message received:', event.data)
        if (msg.type === 'event') {
            handle_event(msg.event_type, msg.data)
        } else if (msg.type === 'subscribe') {
            console.log('Subscription response received')
            for (const event_type in msg.initial_data) {
                handle_event(event_type as WebsocketEventType, msg.initial_data[event_type])
            }
        }
    }

    ws.onclose = () => {
        console.log('Server connection lost, reconnecting...')
        server_state.server_connected = false
        setTimeout(() => {
            connect(address, subscriptions) // Attempt to reconnect after a delay
        }, 3000) // Reconnect after 3 seconds
    }

    ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        ws.close() // Close the WebSocket on error
    }

    return ws
}

export function startWebsocket(address: string, subscriptions: WebsocketEventType[] = []) {
    return connect(address, subscriptions)
}