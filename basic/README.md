# Forth in $WHATEVER

This is a collection of Forth (or Forth-like) implementations in various languages. It is intended to provide examples of how you can leverage Forth to simplify and add extensibility to your programs.

## Python Implementations

### [simple.py](basic/simple/simple.py?rev=tip)
The simplest thing that could be called a Forth (Mr. Moore will probably disagree with me). However, it provides a useful parser, stack and interface to the host system. Words in this implementation:

* **+** ( a b -- sum) Add two numbers on top of stack.
* **-** ( a b -- difference) Subtracts top number from next on stack.
* **.** ( n --) Pop top of stack and print it.
* **.s** ( --) Print contents of stack (nondestructive).
* **bye** ( --) Exit interpreter.
* **interpret** ( string --) Execute word on top of stack.
* **swap** ( a b -- b a) Swaps top two items on stack.
* **word** ( c -- string) Collect characters in input stream up to character c.

### [fram.py](basic/ram/fram.py?rev=tip)
This implements a semi-traditional Forth dictionary in the RAM array. Words are stored with a name field, link field and code field. Instead of finding things directly with a Python dictionary, the `'` word searches for the xt, or "execution token", to be executed.

In real terms, a little slower, but offers some exciting benefits, which I'll explore later.

* **'** ( name -- xt) Finds word's xt in dictionary.
* **execute** ( xt --) Executes the code at xt.
* **negate** ( n -- -n) Makes number negative (or positive, if you use it twice).
* **words** ( --) Prints list of all words in dictionary.

### [fvars.py](basic/vars/fvars.py?rev=tip)
Now we're getting into memory manipulations with variables and such. This introduces some new stuff in the code field -- a constant or variable is just like any other Forth word, except the code retrieves the values (or address of the values, for variables).

* **!** ( v a --) Store value at address a.
* **,** ( v --) Store v as next value in dictionary.
* **@** ( a -- v) Fetch value from address a.
* **constant** ( name | v --) Create constant with value v.
* **create** ( name | --) Create word name in dictionary.
* **dump** ( start n --) Dump n values starting from RAM address a.
* **variable** ( name | v --) Create variable name, with initial value v.

## References

Some links to more information that will help in understanding why you might do with this and what to do with it once you've got it. If nothing else, please read Walker's essay at the first link.

### Essential

* [ATLAST](https://www.fourmilab.ch/atlast/) -- My first encounter with this concept, written by the legendary John Walker. He explains it better than I can.
* [Starting Forth](https://www.forth.com/starting-forth/) -- Classic Forth tutorial and textbook. Don't be fooled by the illustrations, this book not only teaches you how to use Forth, but actually gives you enough information to write your own as well.
* [Levels of FORTH](https://www.forth.org/literature/forthlev.html) -- Glen Haydon's taxonomy of Forth implementations, slightly outdated, but useful if you're trying to figure out what functionality to implement next.

### Supplemental

* [JONESFORTH](https://github.com/nornagon/jonesforth/blob/master/jonesforth.S) -- A full implementation of Forth, in assembly.
* [Thinking Forth -- A Language and Philosophy for Solving Problems](https://www.forth.com/wp-content/uploads/2018/11/thinking-forth-color.pdf) -- Leo Brodie's masterwork, read this to figure out how to _really_ use your new Forth implementation.

### Historical

* [Forth - The Early Years](https://colorforth.github.io/HOPL.html) -- Potted history of Forth, by its creator, Chuck Moore.
* [Programming a Problem Oriented Language](https://archive.org/details/chuck-moore-forth-book/page/10/mode/2up) -- Unpublished book by Chuck Moore describing early Forth.
