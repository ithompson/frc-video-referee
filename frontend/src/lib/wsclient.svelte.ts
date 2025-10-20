export default class WebSocketClient {
    #ws: WebSocket | null = null;
    #address: string;
    #subscriptions: Partial<Record<string, (data: any) => void>> = {};
    #enabled: boolean = false;
    #pingInterval: number | null = null;
    #pingTimeout: number | null = null;
    #waitingForPong: boolean = false;

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
        this.#stopKeepalive();
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
            this.#startKeepalive();
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
            } else if (msg.type === 'reload') {
                console.log('Server requested reload');
                window.location.reload();
            } else if (msg.type === 'pong') {
                console.log('Received pong response');
                this.#handlePong();
            }
        }

        this.#ws.onclose = () => {
            console.log('Server connection lost, reconnecting...')
            this.state.connected = false;
            this.#ws = null;
            this.#stopKeepalive();
            setTimeout(() => {
                this.connect();
            }, 3000); // Reconnect after 3 seconds
        }

        this.#ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.#ws?.close(); // Close the WebSocket on error
        }
    }

    public sendCommand(command_name: string, data: any) {
        const message = {
            type: 'command',
            command: command_name,
            data: data,
        }
        this.#ws?.send(JSON.stringify(message));
    }

    #startKeepalive() {
        // Send a ping every 30 seconds
        this.#pingInterval = window.setInterval(() => {
            this.#sendPing();
        }, 30000);
    }

    #stopKeepalive() {
        if (this.#pingInterval !== null) {
            clearInterval(this.#pingInterval);
            this.#pingInterval = null;
        }
        if (this.#pingTimeout !== null) {
            clearTimeout(this.#pingTimeout);
            this.#pingTimeout = null;
        }
        this.#waitingForPong = false;
    }

    #sendPing() {
        if (this.#waitingForPong) {
            // Server didn't respond to previous ping, close connection
            console.error('Server not responding to keepalive pings, closing connection');
            this.#ws?.close();
            return;
        }

        const ping = {
            type: 'ping',
            timestamp: Date.now(),
        };
        this.#ws?.send(JSON.stringify(ping));
        this.#waitingForPong = true;

        // Set timeout for pong response (10 seconds)
        this.#pingTimeout = window.setTimeout(() => {
            if (this.#waitingForPong) {
                console.error('No pong response received, closing connection');
                this.#ws?.close();
            }
        }, 10000);
    }

    #handlePong() {
        this.#waitingForPong = false;
        if (this.#pingTimeout !== null) {
            clearTimeout(this.#pingTimeout);
            this.#pingTimeout = null;
        }
    }
}