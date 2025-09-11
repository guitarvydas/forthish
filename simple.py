APP = dict(
    name="Simple Forth-like",
    about="Simple Forth-style parser and evaluator.")

S = []; BUFF = ""; BUFP = 0

def xbye():   "( --) Leave interpreter."; raise SystemExit
def xdot():  "( n --) Print TOS."; print(S.pop())
def xdots(): "( --) Print stack contents."; print(S)
def xadd():  "( a b -- sum)"; S.append(S.pop() + S.pop())
def xswap(): "( a b -- b a)"; x = S[-1]; S[-1] = S[-2]; S[-2] = x
def xsub():  "(a b -- diff)"; xswap(); S.append(S.pop() - S.pop())

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

def xinterpret():
    "( string --) Execute word."
    word = S.pop()
    if not word:
        return
    if word in D:
        D[word]()
    elif word.isdigit():
        S.append(int(word))
    else:
        print(f"{word}?")

D = {"bye": xbye, ".": xdot, ".s": xdots,
     "+": xadd, "swap": xswap, "-": xsub,
     "word": xword, "interpret": xinterpret}

def ok():
    "( --) Interaction loop -- REPL."
    global BUFF, BUFP
    while True:
        BUFF = input("OK ")
        BUFP = 0
        while BUFP < len(BUFF):
            S.append(32)  # ASCII space character.
            xword()
            xinterpret()

if "__main__" == __name__:
    ok()
    
