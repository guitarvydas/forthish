Here are two Python test clients for your server:

## Installation & Usage

**For WebSocket client:**
```bash
pip install websockets
python websocket_client.py --help
```

**For TCP client:**
```bash
python tcp_client.py --help  # No extra dependencies needed
```

## Running Tests

**Test WebSocket server:**
```bash
# Start server in WebSocket mode
SOCKET_TYPE=websocket node server.js

# Run WebSocket tests
python websocket_client.py
python websocket_client.py --interactive  # Interactive mode
python websocket_client.py --host localhost --port 8080
```

**Test TCP server:**
```bash
# Start server in TCP mode  
SOCKET_TYPE=tcp node server.js

# Run TCP tests
python tcp_client.py
python tcp_client.py --interactive  # Interactive mode
python tcp_client.py --host localhost --port 8080
```

## Features

Both clients include:
- **Comprehensive test cases** covering normal operation, edge cases, and error conditions
- **Interactive mode** (`-i` flag) for manual testing
- **Command-line arguments** for host/port configuration
- **Expected vs actual result validation**
- **Error handling** for connection issues

## Test Cases Include:
- Basic string parsing with various terminators
- Multi-character terminators
- Cases where terminator is not found
- Boundary conditions (empty strings, end of buffer)
- Unicode character support
- Invalid input validation
- Error condition testing

The clients will show ✓ PASS or ✗ FAIL for each test case, making it easy to verify your server is working correctly with both socket types.
