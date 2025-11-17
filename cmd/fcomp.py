APP = dict(
    name="Forth Compiling",
    about="Forth that reads from stdin instead of implementing its own REPL",
    fork="Based on ../basic/comp/fcomp.py"
)

import re

S = None
R = None
RAM = None
LAST = None
IP = None
BUFF = None
BUFP = None

class Stack(list):
    def push(my, *items):
        my.extend(items)

class State:
    def __init__ (self):
        self.S = Stack() 
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0

def initialize ():
    global S, R, RAM, LAST, IP, BUFF, BUFP
    St = State ()
    S = St.S
    R = St.R
    RAM = St.RAM
    LAST = St.LAST
    IP = St.IP
    BUFF = ""
    BUFP = 0


def code(name, does, flags=0):
    "( name does /flags/ --) Add new word to RAM dictionary."
    global LAST
    x = len(RAM)       # This is "HERE".
    RAM.append(LAST)   # Link field.
    RAM.append(name)   # Word name.
    RAM.append(flags)  # Flags
    RAM.append(does)   # Code pointer.
    LAST = x

initialize ()

code("drop", lambda : S.pop())  # ( a --) Drop TOS.
code("dup", lambda : S.push(S[-1]))  # ( a -- a a) Duplicate TOS.
code("negate", lambda : S.append(-S.pop()))  # ( n -- -n)
code("emit", lambda : print(chr(int(S.pop())), end=""))  # ( n --) Emit specified character.
code("cr", lambda : print(""))  # ( --) Print carriage return.
code(".", lambda : print(f"{S.pop()} ", end=""))  # ( n --) Print TOS.
code(".s", lambda : print(S))
code("+", lambda : S.append(S.pop() + S.pop()))  # ( a b -- sum)
code("*", lambda : S.append(S.pop() * S.pop()))  # ( a b -- product)
    
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
    found = ""
    while BUFP < len(BUFF):
        x = BUFF[BUFP]
        BUFP += 1
        if want == x:
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
def xdotquote(): "( --) Print string."; xquote(); print(S.pop(), end="")
code('."', xdotquote)
def xcomment(): "( --) Read up to close paren."; S.push(41); xword(); S.pop()
code("(", xcomment, 1)

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
    S.append(32); xword()
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
    "( name -- xt|-1) Search for execution token of word name."
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
    "( name v --) Set value for name."
    RAM[_find(name) + 1] = v

def xwords():
    "( --) Print words in dictionary."
    x = LAST
    while x > -1:
        print(RAM[x + 1], end=" ")
        x = RAM[x]
    print()
code("words", xwords)    

def xexecute():
    "( xt --) Execute xt address."
    try:
        # S.append(S[-1]); S.append(6); xdump()  # Debug.
        RAM[S.pop()]()
    except IndexError:
        print("Stack empty!")
code("execute", xexecute)

def doword():
    "Execute word definition."
    # print(f"Would execute {RAM[W - 2]}...")
    global IP, W
    R.push(IP)
    IP = W + 1

    # Inner interpreter...
    while -1 != RAM[IP]:
        W = RAM[IP]
        ## print(f"-- Doing {W} Stack: {S} RStack: {R}")  # Debug.
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

def xinterpret():
    "( string --) Execute word."
    global IP, W
    state = fvget("state")  # Interpreting or compiling?
    xfind()
    flag = S.pop()
    immediate = (not state) or 1 == flag
    if 0 != flag:
        xt = S.pop()
        if immediate:
            W = xt
            IP = -1  # Dummy to hold place in return stack.
            RAM[xt]()  # Execute code.
        else:
            RAM.append(xt)
    else:
        word = S.pop()
        if re.match(r"^-?\d*$", word):
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

import sys

def main():
    global BUFF, BUFP
    # Read lines from stdin
    for line in sys.stdin:
        # Remove trailing newline
        line = line.rstrip('\n')
        # Assign BUFF to the line
        BUFF = line
        ok = True  # Are things, indeed, ok?
        BUFP = 0
        while ok and BUFP < len(BUFF):
            ok = xinterpret()
    print ("")

if __name__ == "__main__":
    main()        
