APP = dict(
    name="Forth Vars",
    about="Forth with constants and variables.")

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
    n = S.pop(); s = S.pop()
    print(RAM[s:s+n])
code("dump", xdump)

code("@", lambda: S.append(RAM[S.pop()]))
def xstore(): "( n a --) Store n at a."; a = S.pop(); RAM[a] = S.pop()
code("!", xstore)

def xbye(): "( --) Leave interpreter."; raise SystemExit
code("bye",  xbye)

def xtick():
    "( name -- xt) Search for execution token of word name."
    name = S.pop()
    x = LAST
    while x > -1:
        if name == RAM[x]:  # Match!
            S.append(x + 2)  # Push xt.
            break
        else:
            x = RAM[x + 1]  # Get next link.
    else:
        S.append(-1) # We didn't find anything...
code("'", xtick)

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
        RAM[S.pop()]()
    except IndexError:
        print("Stack empty!")
code("execute", xexecute)

def xswap(): "( a b -- b a)"; x = S[-1]; S[-1] = S[-2]; S[-2] = x
code("swap", xswap)
def xsub():  "(a b -- diff)"; xswap(); S.append(S.pop() - S.pop())
code("-",    xsub)

code("negate", lambda : S.append(-S.pop()))  # ( n -- -n)
code(".",    lambda : print(S.pop()))  # ( n --) Print TOS.
code(".s",   lambda : print(S))  # ( --) Print stack contents.
code("+",    lambda : S.append(S.pop() + S.pop()))  # ( a b -- sum)

def xword():
    "(char -- string) Read in string delimited by char."
    global BUFP
    want = chr(S.pop())
    found = ""
    while BUFP < len(BUFF):
        x = BUFF[BUFP]
        BUFP += 1
        if want == x:
            break
        else:
            found += x
    S.append(found)
code("word", xword)

def xinterpret():
    "( string --) Execute word."
    word = S.pop()
    if not word:
        return
    S.append(word)
    xtick()  # Find word.
    if S[-1] >= 0:  # Remember! S[-1] is TOS (not S[0]).
        xexecute()
    else:
        S.pop()
        if word.isdigit():
            S.append(int(word))
        else:
            print(f"{word} ?")
code("interpret", xinterpret)

def ok():
    "( --) Interaction loop -- REPL."
    global BUFF, BUFP
    while True:
        BUFF = input("OK ")
        BUFP = 0
        while BUFP < len(BUFF):
            # print(BUFF[BUFP:])  # Debug.
            S.append(32)  # ASCII space character.
            xword()
            xinterpret()

if "__main__" == __name__:
    ok()
