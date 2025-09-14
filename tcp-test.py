#!/usr/bin/env python3
"""
TCP/BSD socket client to test the string parser server.
Usage: python tcp_client.py [host] [port]
"""

import socket
import json
import sys
import argparse
import time

def send_message(sock, data):
    """Send JSON message with newline terminator"""
    message = json.dumps(data) + '\n'
    sock.send(message.encode('utf-8'))

def receive_response(sock):
    """Receive newline-terminated JSON response"""
    buffer = b''
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buffer += chunk
        if b'\n' in buffer:
            break
    
    response = buffer.decode('utf-8').strip()
    return json.loads(response)

def test_parsing(sock, test_cases):
    """Run test cases against the TCP server"""
    print("Running TCP test cases...")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['description']}")
        print(f"Input: {test['input']}")
        
        try:
            # Send request
            send_message(sock, test['input'])
            
            # Receive response
            result = receive_response(sock)
            
            print(f"Output: {result}")
            
            # Check expected result if provided
            if 'expected' in test:
                if result == test['expected']:
                    print("✓ PASS")
                else:
                    print("✗ FAIL")
                    print(f"Expected: {test['expected']}")
            
            # Small delay between tests
            time.sleep(0.1)
            
        except Exception as e:
            print(f"✗ ERROR: {e}")
        
        print("-" * 30)

def interactive_mode(sock):
    """Interactive mode for manual testing"""
    print("\nInteractive mode - Enter JSON or 'quit' to exit")
    print("Example: {\"start\": 0, \"buffer\": \"Hello,World!\", \"terminator\": \",\"}")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
                
            # Try to parse as JSON
            try:
                data = json.loads(user_input)
            except json.JSONDecodeError:
                print("Invalid JSON format")
                continue
            
            # Send to server and get response
            send_message(sock, data)
            result = receive_response(sock)
            
            print(f"Response: {result}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='TCP client for string parser server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8987, help='Server port (default: 8987)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--timeout', type=float, default=5.0, help='Socket timeout in seconds')
    
    args = parser.parse_args()
    
    # Test cases
    test_cases = [
        {
            'description': 'Basic parsing with comma terminator',
            'input': {'start': 0, 'buffer': 'Hello,World!End', 'terminator': ','},
            'expected': {'match': 'Hello', 'next': 6}
        },
        {
            'description': 'Continue parsing from previous position',
            'input': {'start': 6, 'buffer': 'Hello,World!End', 'terminator': '!'},
            'expected': {'match': 'World', 'next': 12}
        },
        {
            'description': 'Terminator not found - return rest of string',
            'input': {'start': 12, 'buffer': 'Hello,World!End', 'terminator': 'X'},
            'expected': {'match': 'End', 'next': 15}
        },
        {
            'description': 'Start at end of string',
            'input': {'start': 15, 'buffer': 'Hello,World!End', 'terminator': ','},
            'expected': {'match': '', 'next': 15}
        },
        {
            'description': 'Multi-character terminator',
            'input': {'start': 0, 'buffer': 'key::value::data', 'terminator': '::'},
            'expected': {'match': 'key', 'next': 5}
        },
        {
            'description': 'Empty string buffer',
            'input': {'start': 0, 'buffer': '', 'terminator': ','},
            'expected': {'match': '', 'next': 0}
        },
        {
            'description': 'Parsing JSON-like structure',
            'input': {'start': 0, 'buffer': '{"name":"value","age":30}', 'terminator': '":"'},
            'expected': {'match': '{"name"', 'next': 9}
        },
        {
            'description': 'Unicode characters',
            'input': {'start': 0, 'buffer': 'Hello🌍World', 'terminator': '🌍'},
            'expected': {'match': 'Hello', 'next': 7}
        },
        {
            'description': 'Invalid start position (negative)',
            'input': {'start': -1, 'buffer': 'Hello', 'terminator': ','}
        },
        {
            'description': 'Invalid input types',
            'input': {'start': 'invalid', 'buffer': 123, 'terminator': None}
        }
    ]
    
    try:
        print(f"Connecting to {args.host}:{args.port}...")
        
        # Create TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(args.timeout)
        
        # Connect to server
        sock.connect((args.host, args.port))
        print("Connected successfully!")
        
        if not args.interactive:
            test_parsing(sock, test_cases)
        
        if args.interactive:
            interactive_mode(sock)
            
    except ConnectionRefusedError:
        print(f"Failed to connect to {args.host}:{args.port}")
        print("Make sure the server is running with TCP mode")
        sys.exit(1)
    except socket.timeout:
        print("Connection timed out")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        try:
            sock.close()
            print("Connection closed")
        except:
            pass

if __name__ == "__main__":
    main()
