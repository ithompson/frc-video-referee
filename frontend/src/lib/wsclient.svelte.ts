export default class WebSocketClient {
    #ws: WebSocket | null = null;
    #address: string;
    #subscriptions: Partial<Record<string, (data: any) => void>> = {};
    #enabled: boolean = false;

    state = $state({
        connected: false,
    });

    constructor(address: string) {
        this.#address = address;
    }

    public subscribe(event_type: string, callback: (data: any) => void) {
        this.#subscriptions[event_type] = callback;
        if (this.#ws) {
            this.#ws.send(JSON.stringify({ type: 'subscribe', event_types: [event_type] }));
        }
    }

    public enable() {
        this.#enabled = true;
        this.connect();
    }

    public disable() {
        this.#enabled = false;
        if (this.#ws) {
            this.#ws.close();
            this.#ws = null;
        }
    }

    private connect() {
        if (!this.#enabled || this.#ws) {
            return;
        }

        const full_address = `ws://${this.#address}/api/websocket`;
        console.log('Attempting websocket connection to:', full_address);
        this.#ws = new WebSocket(full_address);

        this.#ws.onopen = () => {
            console.log('WebSocket connection established');
            this.state.connected = true;
            this.#ws?.send(JSON.stringify({ type: 'subscribe', event_types: Object.keys(this.#subscriptions) }));
        }

        this.#ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            console.log('WebSocket message received:', event.data);
            if (msg.type === 'event') {
                // Call callback if event is in the subscriptions
                const callback = this.#subscriptions[msg.event_type];
                if (callback) {
                    callback(msg.data);
                } else {
                    console.warn('Got event type with no registered subscription:', msg.event_type);
                }
            } else if (msg.type === 'subscribe') {
                console.log('Subscription response received');
                for (const [event_type, data] of Object.entries(msg.initial_data)) {
                    const callback = this.#subscriptions[event_type];
                    if (callback) {
                        callback(data);
                    }
                }
            }
        }

        this.#ws.onclose = () => {
            console.log('Server connection lost, reconnecting...')
            this.state.connected = false;
            this.#ws = null;
            setTimeout(() => {
                this.connect();
            }, 3000); // Reconnect after 3 seconds
        }

        this.#ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.#ws?.close(); // Close the WebSocket on error
        }
    }

    public send(message: any) {
        this.#ws?.send(JSON.stringify(message));
    }
}