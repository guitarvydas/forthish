const net = require('net');
const WebSocket = require('ws');

class StringParserServer {
    constructor(options = {}) {
        this.port = options.port || 8987;
        this.socketType = options.socketType || 'websocket'; // 'websocket' or 'tcp'
        this.server = null;
    }

    // Core parsing logic (shared between both socket types)
    parseString(start, buffer, terminator) {
        // Validate inputs
        if (typeof buffer !== 'string' || 
            typeof start !== 'number' || 
            typeof terminator !== 'string') {
            return {
                error: 'Invalid input types. Expected: {start: number, buffer: string, terminator: string}'
            };
        }

        if (start < 0 || start > buffer.length) {
            return {
                error: 'Start position out of bounds'
            };
        }

        // Find terminator starting from start position
        const searchString = buffer.substring(start);
        const terminatorIndex = searchString.indexOf(terminator);

        let match;
        let next;

        if (terminatorIndex === -1) {
            // Terminator not found - return rest of string
            match = searchString;
            next = buffer.length; // String exhausted
        } else {
            // Terminator found - return string up to (but not including) terminator
            match = searchString.substring(0, terminatorIndex);
            next = start + terminatorIndex + terminator.length;
            
            // Ensure next doesn't exceed string length
            if (next > buffer.length) {
                next = buffer.length;
            }
        }

        return {
            match: match,
            next: next
        };
    }

    // Handle message processing (shared logic)
    processMessage(messageData, sendResponse) {
        try {
            const data = JSON.parse(messageData);
            const { start, buffer, terminator } = data;
            
            const result = this.parseString(start, buffer, terminator);
            sendResponse(JSON.stringify(result));
            
        } catch (error) {
            sendResponse(JSON.stringify({
                error: 'Invalid JSON format or processing error: ' + error.message
            }));
        }
    }

    // WebSocket server implementation
    startWebSocketServer() {
        this.server = new WebSocket.Server({ port: this.port });
        
        console.log(`WebSocket server started on port ${this.port}`);
        
        this.server.on('connection', (ws) => {
            console.log('WebSocket client connected');
            
            ws.on('message', (message) => {
                this.processMessage(message.toString(), (response) => {
                    ws.send(response);
                });
            });
            
            ws.on('close', () => {
                console.log('WebSocket client disconnected');
            });
            
            ws.on('error', (error) => {
                console.error('WebSocket error:', error);
            });
        });
    }

    // TCP/BSD socket server implementation
    startTcpServer() {
        this.server = net.createServer((socket) => {
            console.log('TCP client connected');
            
            let buffer = '';
            
            socket.on('data', (data) => {
                buffer += data.toString();
                
                // Process complete JSON messages (assuming newline-delimited)
                let newlineIndex;
                while ((newlineIndex = buffer.indexOf('\n')) !== -1) {
                    const message = buffer.substring(0, newlineIndex);
                    buffer = buffer.substring(newlineIndex + 1);
                    
                    if (message.trim()) {
                        this.processMessage(message, (response) => {
                            socket.write(response + '\n');
                        });
                    }
                }
            });
            
            socket.on('close', () => {
                console.log('TCP client disconnected');
            });
            
            socket.on('error', (error) => {
                console.error('TCP socket error:', error);
            });
        });
        
        this.server.listen(this.port, () => {
            console.log(`TCP server started on port ${this.port}`);
        });
    }

    // Start the appropriate server type
    start() {
        if (this.socketType === 'websocket') {
            this.startWebSocketServer();
        } else if (this.socketType === 'tcp') {
            this.startTcpServer();
        } else {
            throw new Error('Invalid socket type. Use "websocket" or "tcp"');
        }
    }

    // Stop the server
    stop() {
        if (this.server) {
            if (this.socketType === 'websocket') {
                this.server.close();
            } else {
                this.server.close();
            }
            console.log('Server stopped');
        }
    }
}

// Configuration - change these parameters as needed
const CONFIG = {
    port: 8987,
    socketType: process.env.SOCKET_TYPE || 'websocket' // 'websocket' or 'tcp'
};

// Create and start server
const server = new StringParserServer(CONFIG);
server.start();

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down server...');
    server.stop();
    process.exit(0);
});

// Usage examples
console.log(`
Server running with ${CONFIG.socketType.toUpperCase()} on port ${CONFIG.port}

=== WebSocket Usage ===
Connect to ws://localhost:${CONFIG.port}
Send: {"start": 0, "buffer": "Hello,World!End", "terminator": ","}
Receive: {"match": "Hello", "next": 6}

=== TCP Usage ===
Connect to localhost:${CONFIG.port}
Send: {"start": 0, "buffer": "Hello,World!End", "terminator": ","}\n
Receive: {"match": "Hello", "next": 6}\n

Environment variable SOCKET_TYPE can be set to 'websocket' or 'tcp'
Example: SOCKET_TYPE=tcp node server.js
`);
