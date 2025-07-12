// FRC Video Referee - JavaScript Client

class WebSocketClient {
    constructor() {
        this.socket = null;
        this.reconnectInterval = 5000;
        this.maxReconnectAttempts = 5;
        this.reconnectAttempts = 0;
        this.isConnected = false;
        
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
        this.messagesDiv = document.getElementById('messages');
        this.messageInput = document.getElementById('messageInput');
        
        this.connect();
        this.setupEventListeners();
    }
    
    connect() {
        try {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = () => {
                this.onOpen();
            };
            
            this.socket.onmessage = (event) => {
                this.onMessage(event);
            };
            
            this.socket.onclose = () => {
                this.onClose();
            };
            
            this.socket.onerror = (error) => {
                this.onError(error);
            };
            
        } catch (error) {
            console.error('WebSocket connection failed:', error);
            this.updateStatus('disconnected', 'Connection failed');
        }
    }
    
    onOpen() {
        console.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.updateStatus('connected', 'Connected');
        this.addMessage('Connected to server', 'system');
    }
    
    onMessage(event) {
        console.log('Received message:', event.data);
        this.addMessage(event.data, 'received');
    }
    
    onClose() {
        console.log('WebSocket disconnected');
        this.isConnected = false;
        this.updateStatus('disconnected', 'Disconnected');
        this.addMessage('Disconnected from server', 'system');
        
        // Attempt to reconnect
        this.attemptReconnect();
    }
    
    onError(error) {
        console.error('WebSocket error:', error);
        this.updateStatus('disconnected', 'Connection error');
        this.addMessage('Connection error occurred', 'system');
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            this.updateStatus('connecting', `Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            this.updateStatus('disconnected', 'Max reconnection attempts reached');
            this.addMessage('Max reconnection attempts reached', 'system');
        }
    }
    
    updateStatus(status, text) {
        const dot = this.statusIndicator.querySelector('.dot');
        const statusText = this.statusText;
        
        // Remove existing status classes
        dot.classList.remove('connected', 'disconnected', 'connecting');
        
        // Add new status class
        dot.classList.add(status);
        statusText.textContent = text;
    }
    
    addMessage(message, type = 'received') {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        messageElement.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
        
        this.messagesDiv.appendChild(messageElement);
        this.messagesDiv.scrollTop = this.messagesDiv.scrollHeight;
        
        // Keep only the last 50 messages
        while (this.messagesDiv.children.length > 50) {
            this.messagesDiv.removeChild(this.messagesDiv.firstChild);
        }
    }
    
    sendMessage(message) {
        if (this.isConnected && this.socket) {
            this.socket.send(message);
            this.addMessage(message, 'sent');
            return true;
        } else {
            this.addMessage('Cannot send message: not connected', 'system');
            return false;
        }
    }
    
    setupEventListeners() {
        // Enter key to send message
        this.messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Check server status periodically
        setInterval(() => {
            this.checkServerStatus();
        }, 30000); // Check every 30 seconds
    }
    
    async checkServerStatus() {
        try {
            const response = await fetch('/api/status', {
                method: 'GET',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:password') // Basic auth
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('Server status:', data);
            }
        } catch (error) {
            console.error('Failed to check server status:', error);
        }
    }
}

// Global functions
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (message) {
        if (window.wsClient.sendMessage(message)) {
            messageInput.value = '';
        }
    }
}

// Initialize WebSocket client when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing FRC Video Referee client...');
    window.wsClient = new WebSocketClient();
    
    // Initial status check
    window.wsClient.checkServerStatus();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('Page hidden');
    } else {
        console.log('Page visible');
        // Reconnect if needed when page becomes visible
        if (!window.wsClient.isConnected) {
            window.wsClient.connect();
        }
    }
});

// Handle window beforeunload
window.addEventListener('beforeunload', () => {
    if (window.wsClient && window.wsClient.socket) {
        window.wsClient.socket.close();
    }
});
