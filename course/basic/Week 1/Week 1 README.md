### [simple.py](simple.py?rev=tip)
#### Usage
	```
	python3 simple.py
	```
#### Description
The simplest thing that could be called a Forth (Mr. Moore will probably disagree with me). However, it provides a useful parser, stack and interface to the host system. Words in this implementation:

* **+** ( a b -- sum) Add two numbers on top of stack.
* **-** ( a b -- difference) Subtracts top number from next on stack.
* **.** ( n --) Pop top of stack and print it.
* **.s** ( --) Print contents of stack (nondestructive).
* **bye** ( --) Exit interpreter.
* **interpret** ( string --) Execute word on top of stack.
* **swap** ( a b -- b a) Swaps top two items on stack.
* **word** ( c -- string) Collect characters in input stream up to character c.