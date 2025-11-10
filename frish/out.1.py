Stack = []; BUFF = ""; BUFP = 0
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
    # ( --) Leave interpreter

    raise SystemExit                                   #line 1

def xdot ():
    # ( n --) Print TOS
    print (Stack.pop (), end="")
    print ()                                           #line 2

def xdots ():
    # ( --) Print stack contents
    print (Stack, end="")
    print ()                                           #line 3

def xadd ():                                           #line 4
    # ( a b -- sum)                                    #line 5

    A = Stack.pop ()                                   #line 6

    B = Stack.pop ()                                   #line 7
    Stack.append ( A+ B)                               #line 8#line 9

def xsub ():                                           #line 10
    # ( a b -- diff)                                   #line 11

    A = Stack.pop ()                                   #line 12

    B = Stack.pop ()                                   #line 13
    Stack.append ( A- B)                               #line 14#line 15

def xswap ():                                          #line 16
    # ( a b -- b a)                                    #line 17
    x = Stack [-1]
    Stack [-1] = Stack [-2]
    Stack [-2] = x                                     #line 18#line 22#line 23

def xword ():                                          #line 24
    # (char -- string) Read in string delimited by char #line 25

    wanted = chr(Stack.pop ())                         #line 26

    global BUFF, BUFP
    found = ""
    while BUFP < len(BUFF):
        x = BUFF[BUFP]
        BUFP += 1
        if wanted == x:
            break
        else:
            found += x
    Stack.append(found)
                                                       #line 27#line 28#line 29

def xinterpret ():                                     #line 30
    # ( string --) Execute word                        #line 31

    word = Stack.pop ()
    if(  word):                                        #line 35

        found, subr = Lookup (subrs,  word)            #line 36
        if  found:                                     #line 37
            subr()                                     #line 38
        elif  word.isdigit():
            Stack.append (int ( i))
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
def ok ():                                             #line 60
    # ( --) Interaction loop -- REPL                   #line 61

    blank =  32                                        #line 62
    while  True:                                       #line 63

        global BUFF, BUFP
        BUFF = input("OK ")
        BUFP = 0
                                                       #line 64
        while not (BUFP >= len(BUFF)):                 #line 65
            Stack.append ( blank)                      #line 66
            xword()                                    #line 67
            xinterpret()                               #line 68#line 69#line 70#line 71#line 72
ok()                                                   #line 73#line 74