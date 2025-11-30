all: main

main: build
	./run.bash out.1.py

build:
	rm -f out.*
	rm -f *.json
	node pbp/das/das2json.mjs frish.drawio
	./check-for-span-error.bash frish.drawio.json
	python3 main.py . 'forthish.frish' main frish.drawio.json | node ./pbp/kernel/splitoutput.js

dev:
	rm -f out.*
	rm -f *.json
	node pbp/das/das2json.mjs frish.drawio
	./check-for-span-error.bash frish.drawio.json
	python3 main.py . 'test.frish' main frish.drawio.json | node ./pbp/kernel/splitoutput.js
	#                  ^^^^^^^^^^
	./run.bash out.1.py

