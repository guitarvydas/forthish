all: testws

install:
	python3 -m venv ./venv
	source venv/bin/activate
	python3 -m pip install websockets
	npm install ws

testws:
	./testws.bash
	killall node

testbsdsock:
	./testtcp.bash
	killall node

kill:
	killall node
