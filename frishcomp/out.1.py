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

class StateClass:
    def __init__ (self):
        self.S = Stack()
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0
        self.compiling = False

State = StateClass ()


def code (name,flags,does):
    global State                                       #line 1
    # Add new word to RAM dictionary. We create a word (Forth "object") in RAM with 5 fields and extend the⎩2⎭
    the dictionary by linking back to the head of the dictionary list #line 3
    x =  len( State.RAM)                               #line 4#line 5
    State.RAM.append( State.LAST)
    # (LFA) link to previous word in dictionary list   #line 6
    State.RAM.append( name)
    # (NFA) name of word                               #line 7
    State.RAM.append( flags)
    #       0 = normal word, 1 = immediate word        #line 8
    State.RAM.append( does)
    # (CFA) function pointer that points to code that executes the word #line 9#line 10
    State.LAST =  x
    # LAST is the pointer to the head of the dictionary list, set it to point to⎩11⎭
    this new word                                      #line 12#line 13#line 14

def xdrop ():
    global State                                       #line 15
    # ( a -- )                                         #line 16
    State.S.pop ()                                     #line 17#line 18#line 19
code("drop", xdrop, 0)

def xdup ():
    global State                                       #line 20
    # ( a -- a a )                                     #line 21

    A = State.S.pop ()                                 #line 22
    State.S.append ( A)                                #line 23
    State.S.append ( A)                                #line 24#line 25#line 26
code("dup", xdup, 0)

def xnegate ():
    global State                                       #line 27
    # ( n -- (-n) )                                    #line 28

    n = State.S.pop ()                                 #line 29
    State.S.append ( -n)                               #line 30#line 31#line 32
code("negate", xnegate, 0)

def xemit ():
    global State                                       #line 33
    # ( c -- ) emit specified character                #line 34

    c = State.S.pop ()                                 #line 35
    print (chr (int ( c))), end="")                    #line 36#line 37#line 38
code("emit", xemit, 0)

def xcr ():
    global State
    print ()                                           #line 39
code("cr", xcr, 0)

def xdot ():
    global State
    # ( n --) Print TOS
    print (State.S.pop (), end="")
    print ()                                           #line 40
code(".", xdot, 0)

def xdots ():
    global State
    # ( --) Print stack contents
    print (State.S, end="")
    print ()                                           #line 41#line 42
code(".s", xdots, 0)

def xadd ():
    global State                                       #line 43
    # ( a b -- sum)                                    #line 44

    B = State.S.pop ()                                 #line 45

    A = State.S.pop ()                                 #line 46
    State.S.append ( A+ B)                             #line 47#line 48#line 49
code("+", xadd, 0)

def xmul ():
    global State                                       #line 50
    # ( a b -- product )                               #line 51

    B = State.S.pop ()                                 #line 52

    A = State.S.pop ()                                 #line 53
    State.S.append ( A* B)                             #line 54#line 55#line 56
code("*", xmul, 0)

def xeq ():
    global State                                       #line 57
    # ( a b -- bool )                                  #line 58

    B = State.S.pop ()                                 #line 59

    A = State.S.pop ()                                 #line 60
    State.S.append ( A ==  B)                          #line 61#line 62#line 63
code("=", xeq, 0)

def xlt ():
    global State                                       #line 64
    # ( a b -- bool )                                  #line 65

    B = State.S.pop ()                                 #line 66

    A = State.S.pop ()                                 #line 67
    State.S.append ( A <  B)                           #line 68#line 69#line 70
code("<", xlt, 0)

def xgt ():
    global State                                       #line 71
    # ( a b -- bool )                                  #line 72

    B = State.S.pop ()                                 #line 73

    A = State.S.pop ()                                 #line 74
    State.S.append ( A >  B)                           #line 75#line 76#line 77
code(">", xgt, 0)

def xeq0 ():
    global State                                       #line 78
    # ( a -- bool )                                    #line 79

    a = State.S.pop ()                                 #line 80
    State.S.append ( a ==  0)                          #line 81#line 82#line 83
code("0=", xeq0, 0)

def x0lt ():
    global State                                       #line 84
    # ( a -- bool )                                    #line 85

    a = State.S.pop ()                                 #line 86
    State.S.append ( 0 <  a)                           #line 87#line 88#line 89
code("0<", x0lt, 0)

def x0gt ():
    global State                                       #line 90
    # ( a -- bool )                                    #line 91

    a = State.S.pop ()                                 #line 92
    State.S.append ( 0 >  a)                           #line 93#line 94#line 95
code("0>", x0gt, 0)

def xnot ():
    global State                                       #line 96
    # ( a -- bool )                                    #line 97

    a = State.S.pop ()                                 #line 98
    State.S.append (not  a)                            #line 99#line 100#line 101
code("not", xnot, 0)

def xand ():
    global State                                       #line 102
    # ( a b -- bool )                                  #line 103

    b = State.S.pop ()                                 #line 104

    a = State.S.pop ()                                 #line 105
    State.S.append ( a and  b)                         #line 106#line 107#line 108
code("and", xand, 0)

def xor ():
    global State                                       #line 109
    # ( a b -- bool )                                  #line 110

    b = State.S.pop ()                                 #line 111

    a = State.S.pop ()                                 #line 112
    State.S.append ( a or  b)                          #line 113#line 114#line 115
code("or", xor, 0)

def xStoR ():
    global State                                       #line 116
    # ( a --  )                                        #line 117

    a = State.S.pop ()                                 #line 118
    State.R.append ( a)                                #line 119#line 120#line 121
code(">r", xStoR, 0)

def xRtoS ():
    global State                                       #line 122
    # ( -- x )                                         #line 123

    x = State.R.pop ()                                 #line 124
    State.S.append ( x)                                #line 125#line 126#line 127
code("r>", xRtoS, 0)

def xi ():
    global State                                       #line 128
    # ( -- i ) get current loop index from R stack     #line 129

    i = State.R [-1]                                   #line 130
    State.S.append ( i)                                #line 131#line 132#line 133
code("i", xi, 0)

def xi ():
    global State                                       #line 134
    # ( -- i ) get outer loop limit from R stack       #line 135

    i = %rsecond                                       #line 136
    State.S.append ( i)                                #line 137#line 138#line 139
code("i'", xi, 0)

def xj ():
    global State                                       #line 140
    # ( -- j ) get outer loop index from R stack       #line 141

    j = State.R [-3]                                   #line 142
    State.S.append ( j)                                #line 143#line 144#line 145
code("j", xj, 0)

def xswap ():
    global State                                       #line 146
    # ( a b -- b a)                                    #line 147

    B = State.S.pop ()                                 #line 148

    A = State.S.pop ()                                 #line 149
    State.S.append ( B)                                #line 150
    State.S.append ( A)                                #line 151#line 152
code("swap", xswap, 0)

def xsub ():
    global State                                       #line 153
    # ( a b -- diff)                                   #line 154

    B = State.S.pop ()                                 #line 155

    A = State.S.pop ()                                 #line 156
    State.S.append ( A- B)                             #line 157#line 158
code("-", xsub, 0)

def xdiv ():
    global State                                       #line 159
    # ( a b -- div)                                    #line 160 xswap()#line 161

    B = State.S.pop ()                                 #line 162

    A = State.S.pop ()                                 #line 163
    State.S.append( B [A])                             #line 164#line 165#line 166
code("/", xdiv, 0)

def xword ():
    global State                                       #line 167
    # (char -- string) Read in string delimited by char #line 168

    wanted = chr(State.S.pop ())                       #line 169

    found = ""
    while State.BUFP < len(State.BUFF):
        x = State.BUFF[State.BUFP]
        State.BUFP += 1
        if wanted == x:
            break
        else:
            found += x
    State.S.append(found)
                                                       #line 170#line 171#line 172
code("word", xword, 0)

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 173
# This sin allows it to be used the same way compiling or interactive. #line 174
def xquote ():
    global State                                       #line 175
    # ( -- string) Read up to closing dquote, push to stack #line 176
    # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 177
    # E.G. " abc"                                      #line 178

    DQ =  34                                           #line 179
    State.S.append ( DQ)                               #line 180 xword()#line 181
    if State.compiling:                                #line 182
        literalize()                                   #line 183#line 184#line 185#line 186
code("'", xquote, 0)

def xdotquote ():
    global State                                       #line 187
    # ( --) Print string.                              #line 188 xquote()#line 189
    print (State.S.pop (), end="")                     #line 190#line 191#line 192
code(".'", xdotquote, 0)
                                                       #line 193#line 194
def xdoliteral ():
    global State                                       #line 195
    #⎩196⎭
    Inside definitions only, pushes compiled literal to stack ⎩197⎭
    ⎩198⎭
    Certain Forth words are only applicable inside compiled sequences of subroutines ⎩199⎭
    Literals are handled in different ways when interpreted when in the REPL vs⎩200⎭
    compiled into sequences of subrs ⎩201⎭
    In the REPL, when we encounter a literal, we simply push it onto the stack ⎩202⎭
    In the compiler, though, we have to create an instruction that pushes ⎩203⎭
    the literal onto the stack. ⎩204⎭
    Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩205⎭
    bake in code that pushes the literal when the time comes to run the sequence. ⎩206⎭
    ⎩207⎭
    This word - "(literal)" - is a simple case and one could actually type this ⎩208⎭
    instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩209⎭
    e.g. some control-flow words, tend to be messier and the code below only handles ⎩210⎭
    the compiled aspects and ignores the REPL aspects ⎩211⎭
    ⎩212⎭
    "IP" is the current word index in a sequence of words being compiled. ⎩213⎭
                                                       #line 214

    lit =  RAM [ IP]                                   #line 215
    State.S.append ( lit)                              #line 216
    State.IP =  State.IP+ 1
    # move past this item (the literal) - we're done with it #line 217#line 218#line 219
code("(literal)", xdoliteral, 0)

def literalize ():
    global State                                       #line 220
    # Compile literal into definition.                 #line 221
    Stack.RAM.append( _find( "(literal)"))
    ## Compile address of doliteral.                   #line 222
    Stack.RAM.append(State.S.pop ())
    # # Compile literal value.                         #line 223#line 224#line 225

def xbranch ():
    global State                                       #line 226
    # This instruction appears only inside subroutine sequences, jump to address in next cell #line 227
    # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 228
    IP =  RAM [ IP]                                    #line 229
    # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 230
    #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 231#line 232#line 233
code("branch", xbranch, 0)

def x0branch ():
    global State                                       #line 234
    # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 235

    test = bool (State.S.pop ())                       #line 236
    if ( test):                                        #line 237
        State.IP =  State.IP+ 1                        #line 238
    else:                                              #line 239
        IP =  RAM [ IP]                                #line 240#line 241#line 242#line 243
code("0branch", x0branch, 0)
                                                       #line 244
# "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩245⎭
work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩246⎭
immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩247⎭
immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩248⎭
                                                       #line 249#line 250#line 251
# IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 252#line 253
# see diagram `compiling-IF-THEN.drawio.png`           #line 254
def xif ():
    global State                                       #line 255
    State.compiling = False
    # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse #line 256
    # Step. 1: generate conditional branch to yet-unknown target1 #line 257

    branchFalseAddress =  _find( "0branch")            #line 258
    Stack.RAM.append( branchFalseAddress)
    # insert branch-if-false opcode (word)             #line 259
    State.R.append (len (Stack.RAM))
    # target1 onto r-stack as memo for later fixup     #line 260

    target1 =  -1                                      #line 261
    Stack.RAM.append( target1)
    # branch target will be fixed up later             #line 262
    # Step. 2: generate code for true branch - return to compiler which will compile the following words #line 263
    # THEN or ELSE will do the fixup of target1        #line 264#line 265#line 266
code("if", xif, 0)

# see diagram `compiling-IF-ELSE-THEN.drawio.png`      #line 267undefined
# see diagrams `compiling-IF-THEN.drawio.png` and `compiling-IF-ELSE-THEN.drawio.png` #line 281undefined
def x_do ():
    global State                                       #line 288
    # ( limit index --) Puts limit and index on return stack. #line 289 xswap()#line 290

    index = State.S.pop ()                             #line 291

    limit = State.S.pop ()                             #line 292
    State.R.append ( index)                            #line 293
    State.R.append ( limit)                            #line 294#line 295#line 296
code("(do)", x_do, 0)
undefined
def x_loop ():
    global State                                       #line 303
    # (  -- f) Determine if loop is done.              #line 304

    index = State.R.pop ()                             #line 305

    limit = State.R.pop ()                             #line 306

    cond = ( index >=  limit)                          #line 307
    State.S.append ( cond)                             #line 308
    if ( cond):
        # clean up rstack if index >= limit            #line 309
        State.R.pop ()                                 #line 310
        State.R.pop ()                                 #line 311#line 312#line 313#line 314
code("(loop)", x_loop, 0)
undefinedundefinedundefinedundefined                   #line 341#line 342
#  "... 123 constant K ..."                            #line 343
#  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 344
#  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 345
#  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩346⎭
gets 123 from its PFA and pushes it onto the stack     #line 347
def xconst ():
    global State                                       #line 348
    #  get next word - the name - from BUFF            #line 349

    blank =  32                                        #line 350
    State.S.append ( blank)                            #line 351 word()#line 352
    #  stack is now: ( NNNN name -- )                  #line 353

    name = State.S.pop ()                              #line 354

    value = State.S.pop ()                             #line 355

    normal =  0                                        #line 356

    fobj =  code( name, normal, doconst)               #line 357
    Stack.RAM.append( value)                           #line 358#line 359#line 360
code("const", xconst, 0)

def doconst ():
    global State
    # method for const                                 #line 361

    parameter =  RAM [ W+ 1]                           #line 362
    State.S.append ( parameter)                        #line 363#line 364#line 365
                                                       #line 366
def docreate ():
    global State                                       #line 367

    parameterAddress =  len( RAM)+ 4                   #line 368
    State.S.append ( parameterAddress)                 #line 369#line 370

def create (name):
    global State                                       #line 371

    normal =  0                                        #line 372
    code( name, normal, docreate)                      #line 373#line 374

def xcreate ():
    global State                                       #line 375

    blank =  32                                        #line 376
    State.S.append ( blank)                            #line 377 word()#line 378

    name = State.S.pop ()                              #line 379
    create( name)                                      #line 380#line 381#line 382
code("create", xcreate, 0)

def comma (value):
    global State                                       #line 383
    RAM.append( value)                                 #line 384#line 385#line 386

def xcomma ():
    global State                                       #line 387
    comma(State.S.pop ())                              #line 388#line 389#line 390
code(",", xcomma, 0)

def fvar (name,value):
    global State                                       #line 391
    create( name)                                      #line 392
    comma( value)                                      #line 393#line 394#line 395

def xvar ():
    global State                                       #line 396

    blank =  32                                        #line 397
    State.S.append ( blank)                            #line 398 word()#line 399

    name = State.S.pop ()                              #line 400

    value = State.S.pop ()                             #line 401
    fvar( name, value)                                 #line 402#line 403#line 404
code("variable", xvar, 0)

def xdump ():
    global State                                       #line 405

    n = int (State.S.pop ())                           #line 406

    start = int (State.S.pop ())                       #line 407
    print ( "----------------------------------------------------------------", end="")#line 408

    a =  start                                         #line 409
    while ( a <  start+( min( n,( len( RAM)- start)))):#line 410
        print ( a, end="")                             #line 411
        print ( ": ", end="")                          #line 412
        print ( RAM [ a], end="")                      #line 413
        print ()                                       #line 414

        a =  a+ 1                                      #line 415#line 416#line 417#line 418
code("dump", xdump, 0)

def xstore ():
    global State                                       #line 419

    b = State.S.pop ()                                 #line 420

    a = State.S.pop ()                                 #line 421
    RAM [ b] =  a                                      #line 422#line 423#line 424
code("!", xstore, 0)

def xbye ():
    global State
    # ( --) Leave interpreter

    raise SystemExit                                   #line 425#line 426
code("bye", xbye, 0)
                                                       #line 427
def _find (name):
    global State                                       #line 428
    # "( name -- cfa|0) Find CFA of word name."        #line 429

    x =  LAST                                          #line 430
    while ( x >=  0):                                  #line 431
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 432
        if ( name ==  RAM [ x+ 1]):
            # # Match!                                 #line 433
            return  x+ 3                               #line 434
        else:                                          #line 435
            x =  RAM [ x]
            # # Get next link.                         #line 436#line 437#line 438
    return  0
    # # Nothing found.                                 #line 439#line 440#line 441

def xfind ():
    global State                                       #line 442
    # "( name | -- (name 0)|(xt 1)|(xt -1)) Search for word name." #line 443
    # 3 possible results: 1. (name 0) if not found, 2. (xt 1) if found and word is immediate, 3. (xt -1) if found and word is normal #line 444
    State.S.append ( 32)                               #line 445 xword()#line 446

    found =  _find( S [ -1])                           #line 447
    if ( 0 ==  found):                                 #line 448
        State.S.append ( 0)                            #line 449
    else:                                              #line 450
        State.S.pop ()
        # # Get rid of name on stack.                  #line 451
        State.S.append ( found)                        #line 452

        immediate =  -1                                #line 453
        if ( RAM [ S [ -1]- 1] &  1):
            immediate =  1                             #line 454
        State.S.append ( immediate)                    #line 455#line 456#line 457#line 458
code("find", xfind, 0)

def xtick ():
    global State                                       #line 459
    # "( name -- xt|-1) Search for execution token of word name." #line 460
    State.S.append ( 32)                               #line 461 xword()#line 462

    name = State.S.pop ()                              #line 463

    found =  _find( name)                              #line 464
    State.S.append ( found)                            #line 465#line 466#line 467
code("'", xtick, 0)

def xnone ():
    global State                                       #line 468

    State.S.append (None)                              #line 469#line 470#line 471
code("None", xnone, 0)

# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩472⎭
these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩473⎭
we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩474⎭
generalization?)                                       #line 475
def fvget (name):
    global State                                       #line 476

    fobjaddress =  _find(State.S.pop ())               #line 477
    return  RAM [ fobjaddress+ 1]                      #line 478#line 479#line 480

def fvset (name,v):
    global State                                       #line 481

    fobjaddress =  _find(State.S.pop ())               #line 482

    namefieldaddess =  fobjaddress+ 1                  #line 483
    RAM [ namefieldaddress] =  v                       #line 484#line 485#line 486
                                                       #line 487
def xwords ():
    global State                                       #line 488
    # print words in dictionary                        #line 489

    x =  LAST                                          #line 490
    while ( x >  -1):                                  #line 491
        print ( RAM [ x+ 1], end="")                   #line 492
        print ( " ", end="")                           #line 493#line 494
    print ()                                           #line 495#line 496#line 497
code("words", xwords, 0)
                                                       #line 498
def xexecute ():
    global State                                       #line 499
    # invoke given word                                #line 500

    wordAddress = State.S.pop ()                       #line 501 wordAddress()#line 502#line 503#line 504
code("execute", xexecute, 0)
                                                       #line 505
def doword ():
    global State                                       #line 506
    #⎩507⎭
    Execute a colon-defined word using indirect threaded code interpretation.⎩508⎭
    ⎩509⎭
    This function implements the inner interpreter for threaded code execution.⎩510⎭
    Threaded code words store their definitions as arrays of code field addresses⎩511⎭
    (CFAs) in the parameter field area (PFA) immediately following the word header.⎩512⎭
    ⎩513⎭
    The execution model maintains two critical registers:⎩514⎭
    ⎩515⎭
    1. IP (Instruction Pointer): References the current position within the⎩516⎭
    threaded code array being interpreted. Since threaded words may invoke⎩517⎭
    other threaded words, IP must be preserved in a reentrant manner via⎩518⎭
    the return stack on each invocation.⎩519⎭
    ⎩520⎭
    2. W (Word Pointer): References the CFA of the currently executing primitive.⎩521⎭
    This global register serves an analogous function to 'self' in object-oriented⎩522⎭
    languages, enabling subroutines to access word header fields through fixed⎩523⎭
    offsets from the CFA.⎩524⎭
    ⎩525⎭
    Optimization rationale: W is positioned to reference the CFA rather than the⎩526⎭
    word header base. This design eliminates offset arithmetic for CFA access—the⎩527⎭
    most frequent header operation—at the cost of requiring offset adjustments⎩528⎭
    for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩529⎭
    deliberate trade-off favoring the common case.⎩530⎭
    ⎩531⎭
    The inner interpreter loop performs the following operations:⎩532⎭
    - Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩533⎭
    - Increment IP to advance through the threaded code array⎩534⎭
    - Execute the primitive via RAM[W]() (performing the second indirection)⎩535⎭
    ⎩536⎭
    By caching the dereferenced CFA in W, we amortize the cost of double⎩537⎭
    indirection: both primitive execution and header field access within⎩538⎭
    subroutines utilize the same cached reference, avoiding redundant⎩539⎭
    dereferences. This is functionally equivalent to parameter passing in⎩540⎭
    object-oriented method invocation, but eliminates the overhead of⎩541⎭
    explicitly passing 'self' to each primitive.⎩542⎭
    ⎩543⎭
    Note: W's state is only defined during primitive execution (within RAM[W]()).⎩544⎭
    Between loop iterations, W may reference a stale CFA, but this is⎩545⎭
    architecturally sound since W is unconditionally updated before each⎩546⎭
    primitive invocation.⎩547⎭
                                                       #line 548#line 549
    State.R.append ( IP)                               #line 550
    IP =  W+ 1                                         #line 551
    while ( -1!= State.RAM [ State.IP]):               #line 552
        W =  State.RAM [ State.IP]                     #line 553
        State.IP =  State.IP+ 1                        #line 554 State.RAM [ State.W]()#line 555#line 556
    IP = State.R.pop ()                                #line 557#line 558#line 559

def xcolon ():
    global State                                       #line 560
    # ( name | --) Start compilation.                  #line 561

    blank =  32                                        #line 562
    State.S.append ( blank)                            #line 563 word()#line 564

    name = State.S.pop ()                              #line 565
    code( name, doword)                                #line 566
    State.compiling = True                             #line 567#line 568#line 569
code(":", xcolon, 0)
undefined
def xinterpret ():
    global State                                       #line 577
    # ( string --) Execute word.                       #line 578#line 579 xfind()#line 580
    # 3 possible results from xfind:⎩581⎭
    1. (name 0) if not found,⎩582⎭
    2. (xt 1) if found and word is immediate,⎩583⎭
    3. (xt -1) if found and word is normal             #line 584

    result = State.S.pop ()

    foundImmediate = ( result ==  1)                   #line 585

    item = State.S.pop ()

    foundNormal = ( result ==  -1)                     #line 586

    notFound = ( result ==  0)                         #line 587
    if ( foundImmediate or  foundNormal):              #line 588
        if State.compiling:

            xt =  item                                 #line 589
            if  foundImmediate:                        #line 590
                State.W =  xt                          #line 591
                State.IP =  -1
                # Dummy to hold place in return stack. #line 592 State.RAM [ xt]()
                # Execute code.                        #line 593
            else:                                      #line 594
                State.RAM.append( xt)                  #line 595#line 596
        else:                                          #line 597
            # not compiling                            #line 598
            State.RAM.append( xt)                      #line 599#line 600
    else:

        word =  item                                   #line 601
        if (re.match(r"^-?d*$", word)):                #line 602
            State.S.append (int ( word))               #line 603
            if State.compiling:                        #line 604 literalize()#line 605#line 606
        elif (re.match(r"^-?d*.?d*$", word)):          #line 607
            State.S.append (float ( word))             #line 608
            if State.compiling:                        #line 609 literalize()#line 610#line 611
        else:                                          #line 612

            State.S.clear()                            #line 613

            State.R.clear()                            #line 614
            print ( word, end="")                      #line 615
            print ( "?", end="")                       #line 616
            print ()                                   #line 617
            return  False                              #line 618#line 619#line 620
    return  True                                       #line 621#line 622#line 623
code("interpret", xinterpret, 0)
                                                       #line 624#line 625#line 626#line 627
# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 628
# This sin allows it to be used the same way compiling or interactive. #line 629undefined#line 640undefined#line 650
def doliteral ():
    global State                                       #line 651
    # Inside definitions only, pushes compiled literal to stack. #line 652
    State.S.append ( RAM [ IP])
    # Push item at IP on stack.                        #line 653
    State.IP =  State.IP+ 1
    # Advance IP past item to continue execution.      #line 654#line 655#line 656

def literalize ():
    global State                                       #line 657
    # Compile literal into definition.                 #line 658
    RAM.append( _find( "(literal)"))
    # Compile address of doliteral.                    #line 659
    RAM.append(State.S.pop ())
    # Compile literal value.                           #line 660#line 661#line 662
                                                       #line 663
def ok ():
    global State                                       #line 664
    # ( --) Interaction loop -- REPL                   #line 665

    blank =  32                                        #line 666
    while  True:                                       #line 667

        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 668
        while not (State.BUFP >= len(State.BUFF)):     #line 669
            if ( xinterpret()):                        #line 670
                print ( " ok", end="")                 #line 671
                print ()                               #line 672#line 673#line 674#line 675#line 676#line 677
ok()                                                   #line 678#line 679