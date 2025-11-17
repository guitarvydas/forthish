class StateClass:
    def __init__ (self):
        self.Stack = []
        self.BUFF = ""
        self.BUFP = 0
State = StateClass ()
def Lookup (dict, key):
    if key == '':
        return None, None
    elif not isinstance(key, str):
        return None, None
    elif key.isdigit ():
        return None, None
    v = dict [key]
    return v is not None, v

def xbye ():
    global State
    # ( --) Leave interpreter

    raise SystemExit                                   #line 1

def xdot ():
    global State
    # ( n --) Print TOS
    print (State.Stack.pop (), end="")
    print ()                                           #line 2

def xdots ():
    global State
    # ( --) Print stack contents
    print (State.Stack, end="")
    print ()                                           #line 3

def xadd ():
    global State                                       #line 4
    # ( a b -- sum)                                    #line 5

    B = State.Stack.pop ()                             #line 6

    A = State.Stack.pop ()                             #line 7
    State.Stack.append ( A+ B)                         #line 8#line 9

def xsub ():
    global State                                       #line 10
    # ( a b -- diff)                                   #line 11

    B = State.Stack.pop ()                             #line 12

    A = State.Stack.pop ()                             #line 13
    State.Stack.append ( A- B)                         #line 14#line 15

def xswap ():
    global State                                       #line 16
    # ( a b -- b a)                                    #line 17

    B = State.Stack.pop ()                             #line 18

    A = State.Stack.pop ()                             #line 19
    State.Stack.append ( B)                            #line 20
    State.Stack.append ( A)                            #line 21#line 22#line 23

def xword ():
    global State                                       #line 24
    # (char -- string) Read in string delimited by char #line 25

    wanted = chr(State.Stack.pop ())                   #line 26

    found = ""
    while State.BUFP < len(State.BUFF):
        x = State.BUFF[State.BUFP]
        State.BUFP += 1
        if wanted == x:
            break
        else:
            found += x
    State.Stack.append(found)
                                                       #line 27#line 28#line 29

def xinterpret ():
    global State                                       #line 30
    # ( string --) Execute word                        #line 31

    word = State.Stack.pop ()
    if(  word):                                        #line 35

        found, subr = Lookup (subrs,  word)            #line 36
        if  found:                                     #line 37
            subr()                                     #line 38
        elif  word.isdigit():
            State.Stack.append (int ( word))
        else:                                          #line 42
            print ( word, end="")                      #line 43
            print ( "?", end="")                       #line 44
            print ()                                   #line 45#line 46#line 48#line 49
subrs = {                                              #line 50

    "bye" : xbye,
    "." : xdot,
    ".s" : xdots,
    "+" : xadd,
    "-" : xsub,
    "swap" : xswap,
    "word" : xword,
    "interpret" : xinterpret,
}
def ok ():
    global State                                       #line 60
    # ( --) Interaction loop -- REPL                   #line 61

    blank =  32                                        #line 62
    while  True:                                       #line 63

        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 64
        while not (State.BUFP >= len(State.BUFF)):     #line 65
            State.Stack.append ( blank)                #line 66
            xword()                                    #line 67
            xinterpret()                               #line 68#line 69#line 70#line 71#line 72
ok()                                                   #line 73#line 74