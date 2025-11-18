---
title: fcomp.py
---

This is just about a fully functional Forth, or at least it demonstrates just about everything you need to have a reasonable implementation.

# Dictionary

These are all the words known to the system. 

## Stack Manipulation

| word | stack         | description                                                |
|------|---------------|------------------------------------------------------------|
| drop | ( a --)       | Discard TOS.                                               |
| dup  | ( a -- a a)   | Duplicate TOS.                                             |
| swap | ( a b -- b a) | Exchange top two values on stack.                          |
| i    | ( -- n)       | Copy first value on return stack to stack.                 |
| i'   | ( -- n)       | Copy second value on return stack to stack.                |
| j    | ( -- n)       | Copy third value on return stack to stack.                 |
| r>   | ( -- n)       | Pop from return stack to stack.                            |
| >r   | ( n --)       | Pop from stack to return stack.                            |
| .s   | ( --)         | Print contents of parameter stack non-destructively.       |
| "    | ( --)         | Read to close quote, push on stack (or compile) as string. |

## Logic and Math Operations

| word   | stack                | description                |
|--------|----------------------|----------------------------|
| or     | ( a b -- f)          | Logical or of a and b.     |
| and    | ( a b -- f)          | Logical and of a and b.    |
| not    | ( x -- 'x)           | Logical not of x.          |
| 0>     | ( a -- f)            | Negative number?           |
| 0<     | ( a -- f)            | Positive number?           |
| 0=     | ( a -- f)            | Equal to zero?             |
| >      | ( a b -- f)          | Is a greater than b?       |
| <      | ( a b -- f)          | Is a less than b?          |
| =      | ( a b -- f)          | Are a and b equivalent?    |
| negate | ( n -- -n)           | Flip sign of n.            |
| +      | ( a b -- sum)        | Add a and b.               |
| *      | ( a b -- product)    | Multiply a times b.        |
| -      | ( a b -- difference) | Subtract b from a.         |
| /      | ( a b -- div)        | Divide a by b.             |
| None   | ( -- None)           | Push Python None to stack. |
| pi     | ( -- pi)             | Constant for value of pi.  |

## Conditionals and Loops

These can only be used inside definitions.

| word  | stack             | description                                         |
|-------|-------------------|-----------------------------------------------------|
| if    | ( f --)           | Eval if flag f is True.                             |
| else  | ( --)             | Provide alternative for if.                         |
| then  | ( --)             | Close out if/else/then clause.                      |
| begin | ( --)             | Start indefinite loop.                              |
| until | ( f --)           | Close indefinite loop with test.                    |
| do    | ( limit index --) | Begin counted loop.                                 |
| loop  | ( --)             | Close do loop.                                      |
| +loop | ( inc --)         | Close counted loop, increments loop index with inc. |

## Control and I/O

| word   | stack       | description                                         |
|--------|-------------|-----------------------------------------------------|
| bye    | ( --)       | Leave interpreter.                                  |
| cr     | ( --)       | Print carriage return.                              |
| emit   | ( char --)  | Print ASCII character for char.                     |
| .      | ( value --) | Print value.                                        |
| ."     | ( --)       | Read to close quote and print immediately.          |
| blk    |             | Variable, current loaded block number.              |
| buffer |             | Variable, current block.                            |
| block  | ( n --)     | Read block data into buffer (if not already there). |
| flush  | ( --)       | Write block in buffer back to disk.                 |
| load   | ( n --)     | Load (if needed) and interpret code from block.     |

A sample block file, `%playground.blk` is included with the
distribution. It's 16 blocks long, or 16 kilobytes. fcomp will use it
for all file I/O operations for now.

## Introspection

Words with leading `$` characters in stack effect diagram indicate a value read from the input stream, e.g. `( $name --)`.

| word      | stack                         | description                                                  |
|-----------|-------------------------------|--------------------------------------------------------------|
| interpret | ( string --)                  | Execute word on top of stack.                                |
| execute   | ( xt --)                      | Executes code at xt.                                         |
| words     | ( --)                         | Print list of all words in dictionary.                       |
| '         | ( $name -- xt/-1)             | Find xt for word name. -1 if not found.                      |
| find      | ( $name -- name 0/xt 1/xt -1) | Search for word name.                                        |
| see       | ( $name --)                   | Decompile word name. Handles constants, codewords and words. |
| dump      | ( a n --)                     | Dump cells starting at a, for n cells.                       |
| word      | ( char -- string)             | Read in string delimited by char.                            |
| ?         | ( a -- v)                     | Get contents of variable.                                    |

## Editor

Yes, believe it or not, fcomp has an editor. Of sorts. This is intended as an example, not a serious programming tool (VSCode, you're safe for now!).

Words with leading `$` characters in stack effect diagram indicate a value read from the input stream, e.g. `( $name --)`.

| word   | stack        | description                              |
|--------|--------------|------------------------------------------|
| line   |              | Variable, current line in block.         |
| cursor |              | Variable, current character in line.     |
| type   | ( --)        | Type out current line with cursor caret. |
| list   | ( n --)      | List specified block (loads if needed).  |
| l      | ( --)        | List current block.                      |
| t      | ( n --)      | Set to specified line and type.          |
| p      | ( $text  --) | Put text to current line.                |

The block editor works on the block in `buffer`, which is pre-allocated to be 1024 characters (as per tradition). This makes for sixteen lines of 64 characters each, which was very convenient back in the old days with much more limited hardware. You can edit with the default RAM buffer, or attach it to a disk block (with `n block`, where `n` is the disk block to use).  These examples use the default `%playground.blk` block file:

```
> 4 list
 0 ( Block #04)                                                    
 1                                                                 
 2 : star ( --) 42 emit ;                                          
 3 : stars ( count --) 0 do star loop ;                            
 4 : dot ( --) star cr ;                                           
 5 : dash ( --) 5 stars cr ;                                       
 6 : f ( --) dash dot dash dot dot ;                               
 7                                                                 
 8 f ( That's how it's done!)                                      
 ...
 ok
> 8 t
^f ( That's how it's done!)                                        8
 ok
> p ." Gimmee an 'F'!"  cr cr  f
 ok
> l
 0 ( Block #04)                                                    
 1                                                                 
 2 : star ( --) 42 emit ;                                          
 3 : stars ( count --) 0 do star loop ;                            
 4 : dot ( --) star cr ;                                           
 5 : dash ( --) 5 stars cr ;                                       
 6 : f ( --) dash dot dash dot dot ;                               
 7                                                                 
 8 ." Gimmee an 'F'!"  cr cr  f                                    
...
 ok
> 4 load
Gimmee an 'F'!

*****
*
*****
*
*
 ok
```

Note that the `list` display is truncated to 8 lines (since the other 8 are blank). Also, if you've made changes like this and you want to save them back to disk, use `flush` to write the current block buffer back out.

## Definitions

Words with leading `$` characters in stack effect diagram indicate a value read from the input stream, e.g. `( $name --)`.

| word      | stack             | description                                               |
|-----------|-------------------|-----------------------------------------------------------|
| state     | ( -- a)           | Variable for interpreter state.                           |
| constant  | ( $name value --) | Add constant to dictionary.                               |
| create    | ( $name --)       | Add label to dictionary.                                  |
| variable  | ( $name value --) | Store value as variable name.                             |
| ,         | ( value --)       | Compile value into next cell in RAM.                      |
| ;         | ( $name --)       | Begin word definition.                                    |
| :         | ( --)             | End word definition.                                      |
| (         | ( --)             | Read up to close paren and discard.                       |
| immediate | ( --)             | Mark most recently compiled word for immediate execution. |
| !         | ( n a --)         | Store n at address a.                                     |
| @         | ( a -- n)         | Retrieve n from address a.                                |

## Fragments

These are used in compiled definitions.

| word      | stack             | description                                                |
|-----------|-------------------|------------------------------------------------------------|
| (literal) | ( --)             | Fragment, marks literal in next cell.                      |
| 0branch   | ( f --)           | Fragment, jump to address in next cell if flag f is False. |
| branch    | ( --)             | Fragment, jump to address in next cell.                    |
| (loop)    | ( -- f)           | Fragment, determines if loop is finished.                  |
| (do)      | ( limit index --) | Fragment, sets up counted loop.                            |

# Defining New Words

Forth is an extensible language, meaning that you can define new procedures, called "words". These act like part of the language itself -- in fact, there's almost no difference between the built-in words and the ones you define. You can even override the definitions of the built-ins.

A word is generally defined using the ":" (colon) to start the definition and the ";" (semicolon, or "semi") to end it:

```
: hi ( --) " Hello, World!" . ;
```

Whatever immediately follows the colon becomes the name of the new definition ("hi"). It doesn't have to be only letters, numbers or underscore (like Python). Forth doesn't care what you call the words, as long as they don't have spaces in them. So, "hi", "Hi!" or "@#Fz" are all fair game (if you speak Martian). 

That bit with the parenthesis following the name might look like function arguments, but it's actually a comment. Open paren tells the interpreter to ignore everything up to the closing paren. It's generally used to provide a "stack picture", which describes what arguments the word expects on the stack and what it will leave behind after its run. So, `( a b -- sum)` indicates that the word expects two arguments, a and b, on the stack, and will leave behind their sum when it finishes running. There are more examples in the table above.

After that, the procedure is spelled out with words just as one might type at the prompt. Because we've told Forth that we're compiling now, these words aren't executed -- they get added to the definition for `hi` incrementally. The semi (`;`) ends the definition and returns to regular interpretation.

If you list the vocabulary with `words`, you'll now see `hi` at the head of the list!

# Conditionals

*Left blank because writer needs sleep.*

# Loops

*Left blank because writer needs sleep.*

# Immediate Words

*Left blank because writer needs sleep.*

# Under the Hood

%fcomp.py is effectively a DTC (Direct Threaded Code) implementation.

The words are stored as elements in an array named `RAM`. I call each element a "cell". This mimics an old-skool Forth using contiguous memory -- except a modern array can store elements of any size, not just an eight bit byte. This makes it convenient to use the datatypes of the host language -- they're stored just like they would be normally -- but also takes advantage of Forth-style compilation and traversal.

A compiled word is at least four cells long:

```
+-----+------+-------+-----+ --------------+
| LFA | name | flags | CFA | parameters... |
+-----+------+-------+-----+ --------------+
```

The first, the Link Field Address, points to the LFA of the previously defined word (or -1) if it's the first. The second cell is the word name as a string. Third is flags, which in this implementation *is* an eight bit byte. Lastly, we have the Code Field Address, which holds a pointer to a host-language native function that does the work.

More cells may be used as "parameters", data to be used by the function in the CFA. For a constant or variable, this would be the actual value stored. For a defined word, it would be a list of CFAs for the words compiled into this word.

Here's a word called `star`. It prints out a single asterisk character:

```
: star 42 emit ;
```

Compiled, it might look like this:

```
+-----+------+-------+----------+--------------------+
| LFA | name | flags | CFA      | parameters...      |
+-----+------+-------+----------+-----+----+----+----+
| 249 | star | 0x00  | <doword> | 123 | 42 | 15 | -1 |
+-----+------+-------+----------+-----+----+----+----+
```

`<doword>` is a reference to the Python function `doword()`, which will iterate through the parameters and call each compiled word in succession. `123` is the CFA of `(literal)`, which intereprets the next cell (`42`) and pushes it on the stack. `15` is the CFA of `emit`, which prints the number on TOS as an ASCII character. The definition is closed out with a `-1`, which tells `doword()` to stop traversing. 

An original-style Forth would terminate the definition with a link or code for `EXIT` instead of `-1`, but for a structured language like Python, it's enough to just mark the end.

## Dumping RAM

You can inspect the RAM with the `dump` word. It takes a starting address and a count and will dump that many cells. It will not go past the end of RAM.

However, while potentially fascinating, it's not terribly productive to just dump random stuff. How can we look at something intentionally? Say a word definition, like `star` above. 

I can use `'` (tick) to find the CFA (code field address) of the word. Then subtract 3 to get the LFA (link field address), which is considered the start of the word record. Compare to the diagram above.

```
> ' star 3 -  8 dump
----------------------------------------------------------------
0254: 249
0255: star
0256: 0
0257: <function doword at 0x0000022DCAA11590>
0258: 123
0259: 42
0260: 15
0261: -1
 ok
```

## Decompiling

A dump is all right, but wouldn't be nicer if the system could just show you the actual compiled word refereces so you don't have to look them up? Yes, yes it would. The `see` word does just that. You can use it on constants and defined words. Everything else (including variables at this point) is assumed to be a codeword (which technically it *is*, but...).

```
> see pi
0176 : <- 0172 | CONSTANT pi | 3.14159
 ok
> see do
0148 | <- 0144 | CODEWORD do | 00000001
 ok
> see stars
0262 : <- 0254 | WORD stars | 00000000
0266 : 0123 - (literal)
0267 : 0
0268 : 0147 - (do)
0269 : 0257 - star
0270 : 0123 - (literal)
0271 : 1
0272 : 0155 - (loop)
0273 : 0131 - 0branch
0274 : 269
 ok
```

The `stars` word is a bit more interesting than `star` example in the section on dump. You can see where literal values (0 for loop index and 1 for loop increment) are compiled in. You'll also perhaps see special words with names in parentheses (the parentheses are part of the word name) that are only used in compiled definitions.

## How Threaded Execution Works

*More to come...*

# Colophon

Generated with `pandoc --css=doc.css -s -o fcomp.html .\fcomp.md`.
