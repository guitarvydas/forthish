# Forth-ish

A small embedded Forth is simple to build using most popular programming languages.

Here, we will look at such a simple implementation in Python. 

This is simple dot pie. As it stands, it contains fewer than 60 lines of Python code and can only invoke built-in subroutines. A later version of the code will show how to "compile" and save little scripts.

In Python, a built-in is called a "word".

The same name - "word" - is used for little scripts.

"Compiled" scripts can invoke other compiled scripts or built-in subroutines.

Built-in subroutines are meant to actually execute some actions. It is possible for built-ins to invoke other scripts or built-ins - this can be seen in the x-interpret subroutine in simple dot pie.

Simple dot pie runs a little repple - a Read Eval Print Loop. It prompts the user and interprets what was typed, using spaces as separators between executable words and numbers.

All executable words in Python affect the stack. Values are popped from the stack and results are pushed onto the stack.

Numbers - integers - are simply pushed onto the stack on the assumption that they will be used by executable words.

For example, to add 1 and 2 together, we would

Step 0 start with nothing

Step 1 push integer 1

Step 2 push integer 2

Step 3 pop two integers

Step 4 add the integers together and push the result

# Simple dot Pie
Simple dot pie just uses a Python dictionary to store functions associated with each word. The dictionary is called D.

Simple dot pie creates three global variables.

The Forth stack, called S.

A string of characters input from the user, called BUFF.

An integer index into the string BUFF. It points to the next character in BUFF that hasn't been processed yet.

In this very simple version, there are only eight built-in subroutines each associated with a string key in the dictionary.

The word "bye" is associated with the subroutine x-bye.

The word *dot* is associated with the subroutine x-dot. Note that the key can be any legal string of characters. In this case, the dot character makes up the string key.

The word *dot-S* is associated with the subroutine x-dots.

The string *plus sign* is associated with the subroutine x-add.

The string *swap* is associated with the subroutine x-swap.

The string *dash* is associated with the subroutine x-sub.

The string *word* is associated with the subroutine x-word.

The string *interpret* is associated with the subroutine x-interpret.

The code for simple dot pie begins with a header dictionary call APP. It gives the name of the project along with some details. As it's written, this is a comment that can be accessed at runtime. Several repple languages use the concept of dock strings, which allows repple users to ask for information about each executable function or word at the repple at runtime. 

Dock strings make it easier to experiment with code in an interactive manner. Compilers tend to delete such information, but, we're seeing the re-introduction of this concept in various languages under the name "introspection".

Of course, you could leave this information out to make the final executable even smaller, but, size doesn't matter as much today as it did in the early days of computing.

Forth uses a convention for commenting about the before and after contents of the stack. 

This Python version uses the same convention. 

The stack comment consists of a parenthesized set of symbols separated by a double dash. 

The *before* stack is shown on the left of the double dash, the *after* stack is shown to the right of the double dash. 

The stack grows from left to right.

The operations of the built-ins x-bye, x-dot, x-dots, x-add, x-swap and x-sub are very simple and are documented in the PDF.

x-word is the input string parser.  It slurps up characters until a separator character is encountered. The actual separator character is not hard-wired into the parser, but is passed on the stack as a parameter to the x-word subroutine.

"ok" is the repple - the Read Eval Print Loop. It repeatedly gets a line of input from the command line, then calls x-word to chunk the line into words. Each word is sequentially provided to the x-interpret subroutine which tries to look up the word in the dictionary and invokes the associated built-in subroutine, or, if the word consists only of digits, it converts the word to an integer and pushes it onto the stack, or, else it prints a very simple error message.

The Python mainline simply calls the "ok" function to run the repple.
# Acknowledgements

Josh Fuller - o o f o e on itch dot I O game jams - wrote the initial version of simple dot pie.

This project is a spin-off from the Toronto Lisp users' group - Torlisp.

# Repositories and Discord and Torlisp Website
