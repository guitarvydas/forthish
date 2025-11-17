#!/bin/bash

while true; do
    read -p "> " line || break
    # Exit on specific command (optional)
    [[ "$line" == "exit" || "$line" == "quit" ]] && break
    echo "$line" >> log
    echo "$line" | python3 fcomp.py $1
done

echo "Goodbye!"
