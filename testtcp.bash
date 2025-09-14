#!/bin/bash
./parse-server.bash
sleep 1
python3 tcp-test.py
