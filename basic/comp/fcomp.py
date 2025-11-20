APP = dict(
    name="Forth Compiling",
    about="Forth that can compile words into the dictionary.")

import re

class Stack(list):
    def push(my, *items):
        my.extend(items)

S = Stack(); R = Stack()
RAM = []; LAST = -1
IP = None; W = None;
BUFF = ""; BUFP = 0
BLKFILE = "playground.blk"

def code(name, does, flags=0):
    "( name does /flags/ --) Add new word to RAM dictionary."
    global LAST
    x = len(RAM)       # This is "HERE".
    RAM.append(LAST)   # Link field.
    RAM.append(name)   # Word name.
    RAM.append(flags)  # Flags
    RAM.append(does)   # Code pointer.
    LAST = x

code("drop",   lambda : S.pop())  # ( a --) Drop TOS.
code("dup",    lambda : S.push(S[-1]))  # ( a -- a a) Duplicate TOS.
code("negate", lambda : S.append(-S.pop()))  # ( n -- -n)
code("emit",   lambda : print(chr(int(S.pop())), end=""))  # ( n --) Emit specified character.
code("cr",     lambda : print(""))  # ( --) Print carriage return.
code(".",      lambda : print(f"{S.pop()} ", end=""))  # ( n --) Print TOS.
code(".s",     lambda : print(f"{' '.join([repr(x) for x in S])} <-Top", end=""))  # ( --) Print stack contents.
code("+",      lambda : S.push(S.pop() + S.pop()))    # ( a b -- sum)
code("*",      lambda : S.push(S.pop() * S.pop()))    # ( a b -- product)
code("=",      lambda : S.push(S.pop() == S.pop()))   # ( a b -- f)
code("<",      lambda : S.push(S.pop() > S.pop()))    # ( a b -- f)
code(">",      lambda : S.push(S.pop() < S.pop()))    # ( a b -- f)
code("not",    lambda : S.push(not S.pop()))          # ( a -- f)
code("and",    lambda : S.push(S.pop() and S.pop()))  # ( a b -- f)
code("or",     lambda : S.push(S.pop() or S.pop()))   # ( a b -- f)
code(">r",     lambda : R.push(S.pop()))              # ( n --)
code("r>",     lambda : S.push(R.pop()))              # ( -- n)
code("i",      lambda : S.push(R[-1]))                # ( -- n)
code("i'",     lambda : S.push(R[-2]))                # ( -- n)
code("j",      lambda : S.push(R[-3]))                # ( -- n)
    
def xswap(): "( a b -- b a)"; x = S[-1]; S[-1] = S[-2]; S[-2] = x
code("swap", xswap)
def xsub():  "(a b -- diff)"; xswap(); S.append(S.pop() - S.pop())
code("-",    xsub)
def xdiv():  "(a b -- div)"; xswap(); S.append(S.pop() / S.pop())
code("/",    xdiv)

def xword():
    "(char -- string) Read in string delimited by char."
    global BUFP
    want = chr(S.pop())
    if ' ' == want:
        want = " \t\n"  # You want whitespace? We'll give you whitespace!
    found = ""
    while BUFP < len(BUFF):
        x = BUFF[BUFP]
        BUFP += 1
        if x in want:
            if 0 == len(found):
                continue
            else:
                break
        else:
            found += x
    S.append(found)
code("word", xword)

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo...
# This sin allows it to be used the same way compiling or interactive.
def xquote():
    "( -- string) Read up to closing quote, push to stack."
    S.push(34); xword()
    if 1 == fvget("state"): literalize()
code('"', xquote, 1)

def doliteral():  # Inside definitions only, pushes compiled literal to stack.
    global IP
    S.push(RAM[IP])  # Push item at IP on stack.
    IP += 1          # Advance IP past item to continue execution.
code("(literal)", doliteral)
def literalize():
    "Compile literal into definition."
    RAM.append(_find("(literal)"))  # Compile address of doliteral.
    RAM.append(S.pop())             # Compile literal value.

def xbranch():
    "Inside definitions, jump to address in next cell."
    global IP
    IP = RAM[IP]  # Move IP to address in cell.
code("branch", xbranch)
def x0branch():
    "Inside definitions, jump to address in next cell, if false."
    global IP
    if bool(S.pop()):
        IP += 1  # Skip over to continue.
    else:
        IP = RAM[IP]  # Move IP to address in cell.
code("0branch", x0branch)

def xif():
    "( f --) Eval if flag is true."
    RAM.append(_find("0branch"))
    R.push(len(RAM))  # Push next address to be updated on else or then.
    RAM.append(-1)    # Placeholder for target jump.
code("if", xif, 1)
def xelse():
    "( --) Begin opposite clause."
    hanging = R.pop()            # Get "if" slot waiting for address.
    RAM.append(_find("branch"))  # Compile in unconditional branch.
    R.push(len(RAM))             # Push next address to be updated on then.
    RAM.append(-1)               # Placeholder for target jump.
    RAM[hanging] = len(RAM)      # Update "if" slot with next address.
code("else", xelse, 1)
def xthen():
    "( --) Close out if/else/then clause."
    RAM[R.pop()] = len(RAM)
code("then", xthen, 1)

def x_do():
    "( limit index --) Puts limit and index on return stack."
    xswap(); R.push(S.pop()); R.push(S.pop())
code("(do)", x_do)
def xdo():
    "( limit index --) Begin counted loop."
    RAM.append(_find("(do)"))  # Push do loop handler.
    R.push(len(RAM))           # Push address to jump back to.
code("do", xdo, 1)    
def x_loop():
    "( -- f) Determine if loop is done."
    R[-1] += S.pop()             # Increment index.
    S.push(R[-1] >= R[-2])       # Test if index matches limit.
    if(S[-1]): R.pop(); R.pop()  # Remove loop variables.
code("(loop)", x_loop)            
def xploop():
    "( --) Close counted loop."
    RAM.append(_find("(loop)"))   # Compile in loop test.
    RAM.append(_find("0branch"))  # Compile in branch check.
    RAM.append(R.pop())           # Address to jump back to.
code("+loop", xploop, 1)
def xloop():
    "( --) Close counted loop."
    S.push(1)
    literalize()                  # Default loop increment for x_loop.
    RAM.append(_find("(loop)"))   # Compile in loop test.
    RAM.append(_find("0branch"))  # Compile in branch check.
    RAM.append(R.pop())           # Address to jump back to.
code("loop", xloop, 1)

code("begin", lambda : R.push(len(RAM)), 1)  # ( --) Start indefinite loop.
def xuntil():
    "( f --) Close indefinite loop with test."
    RAM.append(_find("0branch"))  # Expects result of test on stack.
    RAM.append(R.pop())           # Address to jump back to.
code("until", xuntil, 1)

def doconst():
    "( --) Handle constant in definition."
    S.push(RAM[W + 1])
def const(name, value):
    "( name value --) Add constant to dictionary."
    code(name, doconst)
    RAM.append(value)
def xconst():
    "( value | name --) Add constant to dictionary."
    S.push(32); xword()
    const(S.pop(), S.pop())
code("constant", xconst)

const("pi", 3.14159)

# XXX Rework this to give me a 'dovar()' that I can use with SEE.
def create(name):
    "( name --) Add name to dictionary."
    slot = len(RAM) + 4  # Address immediately following CODE slot.
    code(name, lambda : S.push(slot))
def xcreate():
    "( name | --) Add to dictionary."
    S.push(32); xword(); create(S.pop())
code("create", xcreate)
def comma(value): "( value --) Append to dictionary."; RAM.append(value)
code(",", lambda : comma(S.pop()))
def var(name, value):
    "( name value --) Add variable to dictionary."
    create(name)
    comma(value)
def xvar():
    "( name | value --) Add variable to dictionary."
    S.push(32); xword()
    var(S.pop(), S.pop())
code("variable", xvar)

def xdump():
    "( start n --) Dump RAM."
    n = int(S.pop())
    start = int(S.pop())
    print("-"*64)
    for a in range(start, start + min(n, (len(RAM) - start))):
        print(f"{a:04}: {RAM[a]}")
code("dump", xdump)
def xsee():
    "( name | --) Decompile word definition."
    xtick()
    start = S.pop() - 3
    link = RAM[start]
    name = RAM[start + 1]
    flags = RAM[start + 2]
    does = RAM[start + 3]
    if doconst == does:
        print(f"{start:04} : <- {link:04} | CONSTANT {name} | {RAM[start + 4]}")
    elif doword == does:
        print(f"{start:04} : <- {link:04} | WORD {name} | {flags:08b}")
        c = start + 4
        skip = False  # Skip becaue of literal?
        while -1 != RAM[c]:
            if skip:
                print(f"{c:04} : {repr(RAM[c])}")
                skip = False
            else:
                w = RAM[RAM[c] - 2]
                if w in ["(literal)", "branch", "0branch"]: skip = True
                print(f"{c:04} : {RAM[c]:04} - {w}")
            c += 1
    else:  # Must be a built-in.
        print(f"{start:04} | <- {link:04} | CODEWORD {name} | {flags:08b}")
code("see", xsee)    

code("@", lambda: S.append(RAM[S.pop()]))
def xstore(): "( n a --) Store n at a."; a = S.pop(); RAM[a] = S.pop()
code("!", xstore)

def xbye(): "( --) Leave interpreter."; raise SystemExit
code("bye",  xbye)

def _find(name):
    "( name -- cfa|0) Find CFA of word name."
    x = LAST
    while x >= 0:
        ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug.
        if name == RAM[x + 1]:  # Match!
            return x + 3
        else:
            x = RAM[x]  # Get next link.
    return 0  # Nothing found.
def xfind():
    "( name | -- name 0|xt 1|xt -1) Search for word name."
    S.append(32); xword()
    found = _find(S[-1])
    if 0 == found:
        S.push(0)
    else:
        S.pop()  # Get rid of name on stack.
        S.push(found)
        immediate = -1
        if (RAM[S[-1] - 1] & 1): immediate = 1
        S.push(immediate)
code("find", xfind)

def xtick():
    "( name | -- xt|-1) Search for execution token of word name."
    S.append(32); xword()
    S.push(_find(S.pop()))
code("'", xtick)

code("None", lambda : S.append(None))  # ( -- None) Push Python None on stack.

# Note that these are no longer as "correct" as they could be since
# they are making the assumption that the variable data is stored just
# after the cfa.
def fvget(name):
    "( name -- v) Get value for name."
    return RAM[_find(name) + 1]
# I have a separate set function so I can set something to None.
def fvset(name, v):
    "( name v -- a) Set value for name, return address."
    a = _find(name) + 1
    RAM[a] = v
    return a

def xwords():
    "( --) Print words in dictionary."
    x = LAST
    while x > -1:
        print(RAM[x + 1], end=" ")
        x = RAM[x]
    print()
code("words", xwords)    

# XXX Bug here. Figure out why.
code("execute", lambda : RAM[S.pop()]())  # ( xt --) Execute token.

def doword():
    "Execute word definition."
    global IP, W
    R.push(IP)
    stepping = RAM[W - 1] & 0x04
    if stepping:
        print(f"-- Stepping {RAM[W - 2]}...")
    IP = W + 1
    while -1 != RAM[IP]:  # Inner interpreter...
        if stepping:
            input(f"   IP {IP:2} : {repr(S)} : {repr(R)} : {RAM[RAM[IP] - 2]} > ")
        W = RAM[IP]
        IP += 1
        RAM[W]()
    IP = R.pop()
def xcolon():
    "( name | --) Start compilation."
    S.append(32); xword()
    code(S.pop(), doword)
    fvset("state", 1)  # Start compiling.
code(":", xcolon)
def xsemi():
    "( --) Finish definition."
    RAM.append(-1)  # Marker for end of definition.
    fvset("state", 0)
code(";", xsemi, 1)
def ximmediate(): " ( --) Make most recent word immediate."; RAM[LAST + 2] |= 1
code("immediate", ximmediate)
def xstep():
    "( $word --) Toggle step debugging for $word."
    xtick()
    RAM[S.pop() - 1] ^= (1<<2)
code("step", xstep)

def xinterpret():
    "( string --) Execute word."
    global IP, W
    state = fvget("state")  # Interpreting or compiling?
    xfind()
    flag = S.pop()
    immediate = (not state) or 1 == flag
    if flag & 0x1:
        xt = S.pop()
        if immediate:
            W = xt
            IP = -1  # Dummy to hold place in return stack.
            RAM[xt]()  # Execute code.
        else:
            RAM.append(xt)
    else:
        word = S.pop()
        if not word:
            pass
        elif re.match(r"^-?\d*$", word):
            S.push(int(word))
            if not immediate: literalize()
        elif re.match(r"^-?\d*\.?\d*$", word):
            S.push(float(word))
            if not immediate: literalize()
        else:
            S.clear(); R.clear()
            print(f"{word} ?")
            return False
    return True
code("interpret", xinterpret)

var("state", 0)  # 0 = interpret, 1 = compile

# Block File I/O
var("blk", -1)  # Current block number.
var("buffer", " "*1024)  # Disk buffer.
def xblock():
    "( n --) Read block data into buffer."
    n = S.pop()
    fvset("blk", n)
    with open(BLKFILE, "rb") as f:
        f.seek(n * 1024)
        S.push(fvset("buffer", f.read(1024).decode()))
code("block", xblock)
def xload():
    "( n --) Load contents of block and execute."
    global BUFF, BUFP
    n = S.pop()
    if n != fvget("blk"): # Load if needed.
        S.push(n); xblock()
    stash = [BUFF, BUFP]  # Save current input buffer.
    evaluate(fvget("buffer"))
    [BUFF, BUFP] = stash  # Restore.
code("load", xload)
def xflush():
    "( --) Write block data back to disk."
    blk = fvget("blk")
    if 0 <= blk:
        with open(BLKFILE, "rb+") as f:
            f.seek(blk * 1024)
            f.write(fvget("buffer").encode())
code("flush", xflush)

# "Editor"
var("line", 0)
var("cursor", 0)
def xtype():
    "( --) Type out current line with cursor caret."
    buffer = fvget("buffer")
    l = fvget("line")
    o = l * 64  # Buffer line offset.
    c = fvget("cursor")
    for i in range(64):
        if i == c: print("^", end="")
        print(buffer[o + i], end="")
    print(f"  {l}")
code("type", xtype)
def xlist():
    "( n --) List specified block."
    n = S.pop()
    if n != fvget("blk"):  # Load if needed.
        S.push(n); xblock()
    buffer = fvget("buffer")
    for line in range(16):
        o = line * 64
        print(f"{line:2} {buffer[o:o + 64]}")
code("list", xlist)
def xl(): S.push(fvget("blk")); xlist()
code("l", xl)
def xt():
    "( n --) Set current line to n."
    fvset("line", S.pop())
    xtype()
code("t", xt)
def xp():
    "( text | --) Insert text into line."
    S.push(10); xword()
    buffer = fvget("buffer")
    o = fvget("line") * 64
    text = S.pop()
    fvset("buffer", buffer[:o] + text + buffer[(o + len(text)):])
    fvset("line", (fvget("line") + 1) % 16)  # Move cursor "down".
code("p", xp)    

def evaluate(text):
    "( text -- ok) Execute text, return status."
    global BUFF, BUFP
    BUFF = text; BUFP = 0
    ok = True
    while ok and BUFP < len(BUFF):
        ok = xinterpret()
    return ok

def quit():
    "( --) Interaction loop -- REPL."
    while True:
        if evaluate(input("> ")): print(" ok")

# Elective Words
evaluate("""
: (  41 word drop ;  immediate          ( Now we can have comments!)
: over  ( x y -- x y x)  >r dup r> swap ;
: rot  ( x y z -- y z x)  >r swap r> swap ;
: ?dup  ( n -- n | n n)  dup if dup then ;
: 2dup  ( x y -- x y x y)  >r dup  r> swap over ;
: 0=  ( n -- f)  0 = ;
: 0<  ( n -- f)  0 > ;
: 0>  ( n -- f)  0 < ;
: 1+  ( n -- n+1)  1 + ;
: 1-  ( n -- n-1)  1 - ;
: max  ( x y -- x | y)  2dup  < if swap then  drop ;
: min  ( x y -- x | y)  2dup  > if swap then  drop ;
: ?  ( a -- v)  @ . ;                 ( Print variable value.)
: +!  ( n a --)  dup >r  @ +  r> ! ;  ( Add n to variable at a.)
: leave  ( --)  r> r> drop i >r >r ;  ( Leave do/loop early.)
: space  ( --)  32 emit ;             ( Type single space.)
: spaces  ( n --)  0 do space loop ;  ( Type n spaces.)
: ."  ( string | --)  34 word . ;     ( Print string enclosed in parens.)
""")

if "__main__" == __name__:
    quit()
