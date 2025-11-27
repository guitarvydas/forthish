all: main

main:
	rm -f out.*
	rm -f *.json
	node pbp/das/das2json.mjs frish.drawio
	./check-for-span-error.bash frish.drawio.json
	python3 main.py . 'forthish.frish' main frish.drawio.json | node ./pbp/kernel/splitoutput.js
	@if [ -f out.✗ ]; then \
	  cat out.✗; \
	fi

