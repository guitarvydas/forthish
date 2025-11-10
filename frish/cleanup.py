#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Read from stdin and replace ¶ with newline
src = sys.stdin.read().replace('¶', '\n')

# Write to /tmp/src
with open('/tmp/src', 'w') as f:
    f.write(src)

# Print to stdout
print(src)
