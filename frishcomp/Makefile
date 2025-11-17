all: main

main:
	node pbp/das/das2json.mjs frish.drawio
	rm -f out.*
	python3 main.py . 'forthish.frish' main frish.drawio.json | node ./pbp/kernel/splitoutput.js
	@if [ -f out.✗ ]; then \
	  cat out.✗; \
	fi
