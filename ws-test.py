#!/usr/bin/env python3
"""
WebSocket client to test the string parser server.
Usage: python websocket_client.py [host] [port]
"""

import asyncio
import websockets
import json
import sys
import argparse

async def test_parsing(websocket, test_cases):
    """Run test cases against the WebSocket server"""
    print("Running WebSocket test cases...")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['description']}")
        print(f"Input: {test['input']}")
        
        try:
            # Send request
            await websocket.send(json.dumps(test['input']))
            
            # Receive response
            response = await websocket.recv()
            result = json.loads(response)
            
            print(f"Output: {result}")
            
            # Check expected result if provided
            if 'expected' in test:
                if result == test['expected']:
                    print("✓ PASS")
                else:
                    print("✗ FAIL")
                    print(f"Expected: {test['expected']}")
            
        except Exception as e:
            print(f"✗ ERROR: {e}")
        
        print("-" * 30)

async def interactive_mode(websocket):
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
            
            # Send to server
            await websocket.send(json.dumps(data))
            response = await websocket.recv()
            result = json.loads(response)
            
            print(f"Response: {result}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

async def main():
    parser = argparse.ArgumentParser(description='WebSocket client for string parser server')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8987, help='Server port (default: 8987)')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
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
            'description': 'Empty terminator (should find immediately)',
            'input': {'start': 0, 'buffer': 'Hello', 'terminator': ''},
            'expected': {'match': '', 'next': 0}
        },
        {
            'description': 'Invalid start position (out of bounds)',
            'input': {'start': 100, 'buffer': 'Hello', 'terminator': ','}
        },
        {
            'description': 'Invalid input types',
            'input': {'start': 'invalid', 'buffer': 123, 'terminator': None}
        }
    ]
    
    uri = f"ws://{args.host}:{args.port}"
    
    try:
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("Connected successfully!")
            
            if not args.interactive:
                await test_parsing(websocket, test_cases)
            
            if args.interactive:
                await interactive_mode(websocket)
    
    except ConnectionRefusedError:
        print(f"Failed to connect to {uri}")
        print("Make sure the server is running with WebSocket mode")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Install required package if not available
    try:
        import websockets
    except ImportError:
        print("websockets package not found. Install with:")
        print("pip install websockets")
        sys.exit(1)
    
    asyncio.run(main())
