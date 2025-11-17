# Forth-ish Built For An External REPL

# Future 
Use ASON instead of JSON?

# Serializing the State of the Forth-ish Machine
We will serialize to and from JSON.

What is easy to represent as JSON?
- empty object '{' ws* '}'
- object '{' members '}'
- array
- string
- number (integer or float)
- boolean true
- boolean false
- null

It is not easy to represent a "function" in JSON.
We need to ensure that the forth-ish machine state consists only of JSON-esque entities.
Functions need to be represented as integers. We will take the integers to mean indexes into an array called `RAM`.

If we write our code in Javascript, then we can use OhmJS to parse incoming JSON state. We can use OhmJS from other languages, but we will need to shell-out to a javascript program that uses OhmJS. We could use json libraries, like dumps(), to parse JSON state, but, I want full control of the parser in case we want to extend it to ASON in the future.

# Step 1
Write fcomp.py in frish.

# Step 2
Make frish emit Javascript.

# Step 2
Make all calls indirect, either to a DOCOL or to a builtin.
All functions are represented as integers. How does the machine decide to call a threaded subr vs. a builtin subr?

# Step 3
Remove the REPL code from the machine. Restore machine state from `state.json`. Write machine state to `state.json`.
