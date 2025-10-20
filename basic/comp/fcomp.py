# WIP

APP = dict(
    name="Forth Compiling",
    about="Forth that can compile words into the dictionary.")

S = []; R = []
BUFF = ""; BUFP = 0

RAM = []; LAST = -1; IP = 0
def code(name, code):
    "( name code --) Add new word to RAM dictionary."
    global LAST
    x = len(RAM)
    RAM.append(name)
    RAM.append(LAST)  # Link field.
    RAM.append(code)  # Code pointer.
    LAST = x

def const(name, value):
    "( name value --) Add constant to dictionary."
    slot = len(RAM) + 3
    code(name, lambda : S.append(RAM[slot]))
    RAM.append(value)
def xconst():
    "( value | name --) Add constant to dictionary."
    S.append(32); xword()
    const(S.pop(), S.pop())
code("constant", xconst)

def create(name):
    "( name --) Add name to dictionary."
    slot = len(RAM) + 3
    code(name, lambda : S.append(slot))
def xcreate(): "( name | --) Add to dictionary."; S.append(32); xword(); create(S.pop())
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
    start = S.pop(-2)  # A bit scary...
    print("-"*64)
    for a in range(start, min(start + S.pop(), len(RAM))):
        print(f"{a:04}: {RAM[a]}")
code("dump", xdump)

code("@", lambda: S.append(RAM[S.pop()]))
def xstore(): "( n a --) Store n at a."; a = S.pop(); RAM[a] = S.pop()
code("!", xstore)

def xbye(): "( --) Leave interpreter."; raise SystemExit
code("bye",  xbye)

def _find(name):
    "( name -- ca|-1) Find compilation address of word name."
    x = LAST
    while x > -1:
        if name == RAM[x]:  # Match!
            return x
        else:
            x = RAM[x + 1]  # Get next link.
    return -1  # Nothing found.
def xfind():
    "( name | -- ca) Search for compilation address of word name."
    S.append(32); xword()
    S.append(_find(S.pop()))
code("find", xfind)

def xtick():
    "( name -- name xt) Search for execution token of word name."
    S.append(32); xword()
    found = _find(S[-1])
    if 0 <= found:
        found += 2
    S.append(found)
code("'", xtick)

code("None", lambda : S.append(None))  # ( -- None) Push Python None on stack.

# Note that these are no longer as "correct" as they could be since
# they are making the assumption that the variable data is stored just
# after the cfa.
def fvget(name):
    "( name -- v) Get value for name."
    return RAM[_find(name) + 3]
# I have a separate set function so I can set something to None.
def fvset(name, v):
    "( name v --) Set value for name."
    RAM[_find(name) + 3] = v

def xwords():
    "( --) Print words in dictionary."
    x = LAST
    while x > -1:
        print(RAM[x], end=" ")
        x = RAM[x + 1]
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

def xswap(): "( a b -- b a)"; x = S[-1]; S[-1] = S[-2]; S[-2] = x
code("swap", xswap)
def xsub():  "(a b -- diff)"; xswap(); S.append(S.pop() - S.pop())
code("-",    xsub)

code("negate", lambda : S.append(-S.pop()))  # ( n -- -n)
code(".", lambda : print(S.pop()))  # ( n --) Print TOS.
code(".s", lambda : print(S))  # ( --) Print stack contents.
code("+", lambda : S.append(S.pop() + S.pop()))  # ( a b -- sum)

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

def xcolon():
    "( name | --) Start compilation."
    S.append(32); xword()
    create(S.pop())
    fvset("state", 1)  # Start compiling.
code(":", xcolon)
code(";", lambda : fvset("state", 0))  # ( --) Stop compilation.

def xinterpret():
    "( string --) Execute word."
    state = fvget("state")  # Interpreting or compiling?
    xtick()  # Find word.
    xt = S.pop()
    if 0 <= xt:
        # TODO: The exclusions for semi and None are a hack until I
        # get immediate words working. @oofoe 2025-09-12
        S.pop() # Get rid of name.
        if state and word not in (";", "None"):
            RAM.append(xt)
        else:
            S.append(xt)
            xexecute()
    else:
        word = S.pop()
        if word.isdigit():
            S.append(int(word))
        else:
            print(f"{word} ?")
code("interpret", xinterpret)

var("state", 0)

def ok():
    "( --) Interaction loop -- REPL."
    global BUFF, BUFP
    while True:
        BUFF = input("OK ")
        BUFP = 0
        while BUFP < len(BUFF):
            # print(BUFF[BUFP:])  # Debug.
            xinterpret()

def xquit():
    "( --) REPL."
    while True:
        R = []  # Clear return stack.
        BUFF = input("> ")
        xinterpret()
        print("ok")

if "__main__" == __name__:
    ok()
