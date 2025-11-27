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

def Lookup (dict, key):
    if key == '':
        return None, None
    elif not isinstance(key, str):
        return None, None
    elif key.isdigit ():
        return None, None
    v = dict [key]
    return v is not None, v

def code (name,flags,does,p):
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
    # (CFA) function pointer that points to code that executes the word #line 9
    State.RAM.append( p)
    # (PFA) private data ('p' for 'parameter')         #line 10#line 11
    State.LAST =  x
    # LAST is the pointer to the head of the dictionary list, set it to point to⎩12⎭
    this new word                                      #line 13#line 14#line 15

def xdrop ():
    global State                                       #line 16
    # ( a -- )                                         #line 17
    State.S.pop ()                                     #line 18#line 19#line 20

def xdup ():
    global State                                       #line 21
    # ( a -- a a )                                     #line 22

    A = State.S.pop ()                                 #line 23
    State.S.append ( A)                                #line 24
    State.S.append ( A)                                #line 25#line 26#line 27

def xnegate ():
    global State                                       #line 28
    # ( n -- (-n) )                                    #line 29

    n = State.S.pop ()                                 #line 30
    State.S.append ( -n)                               #line 31#line 32#line 33

def xemit ():
    global State                                       #line 34
    # ( c -- ) emit specified character                #line 35

    c = State.S.pop ()                                 #line 36
    print (chr (int ( c))), end="")                    #line 37#line 38#line 39

def xcr ():
    global State
    print ()                                           #line 40

def xdot ():
    global State
    # ( n --) Print TOS
    print (State.S.pop (), end="")
    print ()                                           #line 41

def xdots ():
    global State
    # ( --) Print stack contents
    print (State.S, end="")
    print ()                                           #line 42#line 43

def xadd ():
    global State                                       #line 44
    # ( a b -- sum)                                    #line 45

    B = State.S.pop ()                                 #line 46

    A = State.S.pop ()                                 #line 47
    State.S.append ( A+ B)                             #line 48#line 49#line 50

def xmul ():
    global State                                       #line 51
    # ( a b -- product )                               #line 52

    B = State.S.pop ()                                 #line 53

    A = State.S.pop ()                                 #line 54
    State.S.append ( A* B)                             #line 55#line 56#line 57

def xeq ():
    global State                                       #line 58
    # ( a b -- bool )                                  #line 59

    B = State.S.pop ()                                 #line 60

    A = State.S.pop ()                                 #line 61
    State.S.append ( A ==  B)                          #line 62#line 63#line 64

def xlt ():
    global State                                       #line 65
    # ( a b -- bool )                                  #line 66

    B = State.S.pop ()                                 #line 67

    A = State.S.pop ()                                 #line 68
    State.S.append ( A <  B)                           #line 69#line 70#line 71

def xgt ():
    global State                                       #line 72
    # ( a b -- bool )                                  #line 73

    B = State.S.pop ()                                 #line 74

    A = State.S.pop ()                                 #line 75
    State.S.append ( A >  B)                           #line 76#line 77#line 78

def xeq0 ():
    global State                                       #line 79
    # ( a -- bool )                                    #line 80

    a = State.S.pop ()                                 #line 81
    State.S.append ( a ==  0)                          #line 82#line 83#line 84

def x0lt ():
    global State                                       #line 85
    # ( a -- bool )                                    #line 86

    a = State.S.pop ()                                 #line 87
    State.S.append ( 0 <  a)                           #line 88#line 89#line 90

def x0gt ():
    global State                                       #line 91
    # ( a -- bool )                                    #line 92

    a = State.S.pop ()                                 #line 93
    State.S.append ( 0 >  a)                           #line 94#line 95#line 96

def xnot ():
    global State                                       #line 97
    # ( a -- bool )                                    #line 98

    a = State.S.pop ()                                 #line 99
    State.S.append (not  a)                            #line 100#line 101#line 102

def xand ():
    global State                                       #line 103
    # ( a b -- bool )                                  #line 104

    b = State.S.pop ()                                 #line 105

    a = State.S.pop ()                                 #line 106
    State.S.append ( a and  b)                         #line 107#line 108#line 109

def xor ():
    global State                                       #line 110
    # ( a b -- bool )                                  #line 111

    b = State.S.pop ()                                 #line 112

    a = State.S.pop ()                                 #line 113
    State.S.append ( a or  b)                          #line 114#line 115#line 116

def xStoR ():
    global State                                       #line 117
    # ( a --  )                                        #line 118

    a = State.S.pop ()                                 #line 119
    State.R.append ( a)                                #line 120#line 121#line 122

def xRtoS ():
    global State                                       #line 123
    # ( -- x )                                         #line 124

    x = State.R.pop ()                                 #line 125
    State.S.append ( x)                                #line 126#line 127#line 128

def xi ():
    global State                                       #line 129
    # ( -- i ) get current loop index from R stack     #line 130

    i = State.R [-1]                                   #line 131
    State.S.append ( i)                                #line 132#line 133#line 134

def xj ():
    global State                                       #line 135
    # ( -- j ) get outer loop index from R stack       #line 136

    j = State.R [-3]                                   #line 137
    State.S.append ( j)                                #line 138#line 139#line 140

def xswap ():
    global State                                       #line 141
    # ( a b -- b a)                                    #line 142

    B = State.S.pop ()                                 #line 143

    A = State.S.pop ()                                 #line 144
    State.S.append ( B)                                #line 145
    State.S.append ( A)                                #line 146#line 147

def xsub ():
    global State                                       #line 148
    # ( a b -- diff)                                   #line 149

    B = State.S.pop ()                                 #line 150

    A = State.S.pop ()                                 #line 151
    State.S.append ( A- B)                             #line 152#line 153

def xdiv ():
    global State                                       #line 154
    # ( a b -- div)                                    #line 155 xswap()#line 156

    B = State.S.pop ()                                 #line 157

    A = State.S.pop ()                                 #line 158
    State.S.append( B [A])                             #line 159#line 160#line 161

def xword ():
    global State                                       #line 162
    # (char -- string) Read in string delimited by char #line 163

    wanted = chr(State.S.pop ())                       #line 164

    found = ""
    while State.BUFP < len(State.BUFF):
        x = State.BUFF[State.BUFP]
        State.BUFP += 1
        if wanted == x:
            break
        else:
            found += x
    State.S.append(found)
                                                       #line 165#line 166#line 167

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 168
# This sin allows it to be used the same way compiling or interactive. #line 169
def xquote ():
    global State                                       #line 170
    # ( -- string) Read up to closing dquote, push to stack #line 171
    # A string in Forth begins with the word " (followed by a space) then all characters up to the next " #line 172
    # E.G. " abc"                                      #line 173

    DQ =  34                                           #line 174
    State.S.append ( DQ)                               #line 175 xword()#line 176
    if State.compiling:                                #line 177
        literalize()                                   #line 178#line 179#line 180#line 181

def xdotquote ():
    global State                                       #line 182
    # ( -- ) parse and print a string                  #line 183
    # ." Hello, World!"                                #line 184 xquote()#line 185

    s = State.S.pop ()                                 #line 186
    print ( s, end="")                                 #line 187#line 188#line 189

def xcomment ():
    global State                                       #line 190
    # ( -- ) parse and discard a comment               #line 191
    # e.g. ( a b c )                                   #line 192

    RPAR =  42                                         #line 193
    State.S.append ( RPAR)                             #line 194 xword()#line 195
    State.S.pop ()                                     #line 196#line 197#line 198
                                                       #line 199
def xdoliteral ():
    global State                                       #line 200
    #⎩201⎭
    Inside definitions only, pushes compiled literal to stack ⎩202⎭
    ⎩203⎭
    Certain Forth words are only applicable inside compiled sequences of subroutines ⎩204⎭
    Literals are handled in different ways when interpreted when in the REPL vs⎩205⎭
    compiled into sequences of subrs ⎩206⎭
    In the REPL, when we encounter a literal, we simply push it onto the stack ⎩207⎭
    In the compiler, though, we have to create an instruction that pushes ⎩208⎭
    the literal onto the stack. ⎩209⎭
    Compiled code doesn't do what the REPL does, we have to hard-wire and ⎩210⎭
    bake in code that pushes the literal when the time comes to run the sequence. ⎩211⎭
    ⎩212⎭
    This word - "(literal)" - is a simple case and one could actually type this ⎩213⎭
    instruction into the REPL, but, that would be redundant.  Other kinds of words, ⎩214⎭
    e.g. some control-flow words, tend to be messier and the code below only handles ⎩215⎭
    the compiled aspects and ignores the REPL aspects ⎩216⎭
    ⎩217⎭
    "IP" is the current word index in a sequence of words being compiled. ⎩218⎭
                                                       #line 219

    lit =  RAM [ IP]                                   #line 220
    State.S.append ( lit)                              #line 221
    State.IP =  State.IP+ 1
    # move past this item (the literal) - we're done with it #line 222#line 223#line 224

def literalize ():
    global State                                       #line 225

    found, address = %  >>>  error - unrecognized builtin "lookup" (with given arguments)  <<<  ("(literal)") #line 226
                                                       #line 227
    RAM.append( address)                               #line 228
    RAM.append(State.S.pop ())                         #line 229#line 230#line 231

def xbranch ():
    global State                                       #line 232
    # This instruction appears only inside subroutine sequences, jump to address in next cell #line 233
    # This instruction is inserted into a subr sequence when compiling control-flow words, like "else" see below) #line 234
    IP =  RAM [ IP]                                    #line 235
    # normally, we just execute an instruction then move the IP sequentially forward by 1 unit, i.e. IP ⇐ IP + 1 #line 236
    #   in this case, though, we explicitly change the IP to some other value and don't just increment it #line 237#line 238#line 239

def x0branch ():
    global State                                       #line 240
    # This instruction appears only inside subroutine sequences, jump on false to address in next cell #line 241

    test = bool (State.S.pop ())                       #line 242
    if ( test):                                        #line 243
        State.IP =  State.IP+ 1                        #line 244
    else:                                              #line 245
        IP =  RAM [ IP]                                #line 246#line 247#line 248#line 249
                                                       #line 250
# "immediate" words are fully operational even when in compile mode. Some (not all) of these words are meant to⎩251⎭
work /only/ in compile mode. At the REPL prompt ("interpret" mode), they produce unwanted results.⎩252⎭
immediate words: xif, xelse, xthen, xquote, xcomment, xsemi⎩253⎭
immediate words that only have meaning in compile mode: xif, xelse, xthen, xsemi⎩254⎭
                                                       #line 255#line 256#line 257
# IF, ELSE and THEN are "immediate" words - they should only be used inside of ":" (colon compiler) #line 258#line 259
# see diagram `compiling-IF-THEN.drawio.png`           #line 260
def xif ():
    global State                                       #line 261
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<
    # This instruction appears only inside subroutine sequences, ( f -- ) compile if test and branchFalse #line 262
    # Step. 1: generate conditional branch to yet-unknown target1 #line 263

    found, branchFalseAddress = %  >>>  error - unrecognized builtin "lookup" (with given arguments)  <<<  ("0branch") #line 264
                                                       #line 265
    RAM.append( branchFalseAddress)
    # insert branch-if-false opcode (word)             #line 266
    State.R.append (%  >>>  error - unrecognized builtin "RAMnext" (with given arguments)  <<<   )
    # target1 onto r-stack as memo for later fixup     #line 267

    target1 =  -1                                      #line 268
    RAM.append( target1)
    # branch target will be fixed up later             #line 269
    # Step. 2: generate code for true branch - return to compiler which will compile the following words #line 270
    # THEN or ELSE will do the fixup of target1        #line 271#line 272#line 273

# see diagram `compiling-IF-ELSE-THEN.drawio.png`      #line 274
def xelse ():
    global State                                       #line 275
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<   #line 276
    # Step. 1: fixup target1 from IF-true, retrieving memo from R-stack #line 277

    target1 = State.R.pop ()                           #line 278
    RAM [ target1] = %  >>>  error - unrecognized builtin "RAMnext" (with given arguments)  <<<   #line 279
    # Step. 2: generate unconditional branch for preceding IF, creating new memo for target2 on R-stack #line 280

    found, brAddress = %  >>>  error - unrecognized builtin "lookup" (with given arguments)  <<<  ("branch") #line 281
    State.R.append (%  >>>  error - unrecognized builtin "RAMnext" (with given arguments)  <<<   )
    # target2 address on R-stack as memo for later fixup #line 282

    target2 =  -1                                      #line 283
    RAM.append( target2)
    # branch target will be fixed up later             #line 284
    # Step. 3: generate code for false branch - return to compiler which will compile the following words #line 285
    # THEN will do the fixup of target2                #line 286#line 287#line 288

# see diagrams `compiling-IF-THEN.drawio.png` and `compiling-IF-ELSE-THEN.drawio.png` #line 289
def xthen ():
    global State                                       #line 290
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<   #line 291
    # Step. 1: fixup target (from IF or from ELSE, above), retrieving memo from R-stack #line 292

    target = State.R.pop ()                            #line 293
    RAM [ target] = %  >>>  error - unrecognized builtin "RAMnext" (with given arguments)  <<<   #line 294#line 295#line 296
                                                       #line 297
#  "... 123 constant K ..."                            #line 298
#  at interpretation time: 123 is on the Stack, we have consumed "constant" from BUFF, BUFF now contains "K ..." #line 299
#  invoke 'word' which parses "K" and pushed it. The stack becomes [... 123 "K"] #line 300
#  pop "K", pop 123, create a new word called 'K' with its PFA set to 123 and its CFA set to a subr that⎩301⎭
gets 123 from its PFA and pushes it onto the stack     #line 302
def xconst ():
    global State                                       #line 303
    #  get next word - the name - from BUFF            #line 304

    blank =  32                                        #line 305
    State.S.append ( blank)                            #line 306 word()#line 307
    #  stack is now: ( NNNN name -- )                  #line 308

    name = State.S.pop ()                              #line 309

    value = State.S.pop ()                             #line 310

    normal =  0                                        #line 311

    fobj =  code( name, normal, doconst)               #line 312
    %  >>>  error - unrecognized builtin "fobjappend" (with given arguments)  <<<  (fobj,value) #line 313#line 314

def doconst ():
    global State
    # method for const                                 #line 315

    parameter =  RAM [ W+ 1]                           #line 316
    State.S.append ( parameter)                        #line 317#line 318#line 319
                                                       #line 320
def docreate ():
    global State                                       #line 321

    parameterAddress =  len( RAM)+ 4                   #line 322
    State.S.append ( parameterAddress)                 #line 323#line 324

def create (name):
    global State                                       #line 325

    normal =  0                                        #line 326
    code( name, normal, docreate)                      #line 327#line 328

def xcreate ():
    global State                                       #line 329

    blank =  32                                        #line 330
    State.S.append ( blank)                            #line 331 word()#line 332

    name = State.S.pop ()                              #line 333
    create( name)                                      #line 334#line 335#line 336

def comma (value):
    global State                                       #line 337
    RAM.append( value)                                 #line 338#line 339#line 340

def xcomma ():
    global State                                       #line 341
    comma(State.S.pop ())                              #line 342#line 343#line 344

def fvar (name,value):
    global State                                       #line 345
    create( name)                                      #line 346
    comma( value)                                      #line 347#line 348#line 349

def xvar ():
    global State                                       #line 350

    blank =  32                                        #line 351
    State.S.append ( blank)                            #line 352 word()#line 353

    name = State.S.pop ()                              #line 354

    value = State.S.pop ()                             #line 355
    fvar( name, value)                                 #line 356#line 357#line 358

def xdump ():
    global State                                       #line 359

    n = int (State.S.pop ())                           #line 360

    start = int (State.S.pop ())                       #line 361
    print ( "----------------------------------------------------------------", end="")#line 362

    a =  start                                         #line 363
    while ( a <  start+%  >>>  error - unrecognized builtin "funcall" (with given arguments)  <<<  (min(n,(%funcalllen(RAM)-start))) ):#line 364
        print ( a, end="")                             #line 365
        print ( ": ", end="")                          #line 366
        print ( RAM [ a], end="")                      #line 367
        print ()                                       #line 368

        a =  a+ 1                                      #line 369#line 370#line 371#line 372

def xstore ():
    global State                                       #line 373

    b = State.S.pop ()                                 #line 374

    a = State.S.pop ()                                 #line 375
    RAM [ b] =  a                                      #line 376#line 377#line 378

def xbye ():
    global State
    # ( --) Leave interpreter

    raise SystemExit                                   #line 379#line 380
                                                       #line 381
def _find (name):
    global State                                       #line 382
    # "( name -- cfa|0) Find CFA of word name."        #line 383

    x =  LAST                                          #line 384
    while ( x >=  0):                                  #line 385
        # ## print(f"-- {x} : {RAM[x]}, {RAM[x + 1]}")  # Debug. #line 386
        if ( name ==  RAM [ x+ 1]):
            # # Match!                                 #line 387
            return  x+ 3                               #line 388
        else:                                          #line 389
            x =  RAM [ x]
            # # Get next link.                         #line 390#line 391#line 392
    return  0
    # # Nothing found.                                 #line 393#line 394#line 395

def xfind ():
    global State                                       #line 396
    # "( name | -- name 0|xt 1|xt -1) Search for word name." #line 397
    State.S.append ( 32)                               #line 398 xword()#line 399

    found =  _find( S [ -1])                           #line 400
    if ( 0 ==  found):                                 #line 401
        State.S.append ( 0)                            #line 402
    else:                                              #line 403
        State.S.pop ()
        # # Get rid of name on stack.                  #line 404
        State.S.append ( found)                        #line 405

        immediate =  -1                                #line 406
        if ( RAM [ S [ -1]- 1] &  1):
            immediate =  1                             #line 407
        State.S.append ( immediate)                    #line 408#line 409#line 410#line 411

def xtick ():
    global State                                       #line 412
    # "( name -- xt|-1) Search for execution token of word name." #line 413
    State.S.append ( 32)                               #line 414 xword()#line 415

    name = State.S.pop ()                              #line 416

    found =  _find( name)                              #line 417
    State.S.append ( found)                            #line 418#line 419#line 420

def xnone ():
    global State                                       #line 421

    State.S.append (None)                              #line 422#line 423#line 424

# fvget and fvset assume that the forth object (word) is a set of contiguous slots, each 1 machine word wide⎩425⎭
these functions use direct integer offsets to access the fields of the fojbect, whereas in higher level languages⎩426⎭
we'd use class fields instead - todo: fix this in the future (or not? at what point is customization better than⎩427⎭
generalization?)                                       #line 428
def fvget (name):
    global State                                       #line 429

    fobjaddress =  _find(State.S.pop ())               #line 430
    return  RAM [ fobjaddress+ 1]                      #line 431#line 432#line 433

def fvset (name,v):
    global State                                       #line 434

    fobjaddress =  _find(State.S.pop ())               #line 435

    namefieldaddess =  fobjaddress+ 1                  #line 436
    RAM [ namefieldaddress] =  v                       #line 437#line 438#line 439
                                                       #line 440
def xwords ():
    global State                                       #line 441
    # print words in dictionary                        #line 442

    x =  LAST                                          #line 443
    while ( x >  -1):                                  #line 444
        print ( RAM [ x+ 1], end="")                   #line 445
        print ( " ", end="")                           #line 446#line 447
    print ()                                           #line 448#line 449#line 450
                                                       #line 451
def xexecute ():
    global State                                       #line 452
    # invoke given word                                #line 453

    wordAddress = State.S.pop ()                       #line 454 wordAddress()#line 455#line 456#line 457
                                                       #line 458
def doword ():
    global State                                       #line 459
    #⎩460⎭
    Execute a colon-defined word using indirect threaded code interpretation.⎩461⎭
    ⎩462⎭
    This function implements the inner interpreter for threaded code execution.⎩463⎭
    Threaded code words store their definitions as arrays of code field addresses⎩464⎭
    (CFAs) in the parameter field area (PFA) immediately following the word header.⎩465⎭
    ⎩466⎭
    The execution model maintains two critical registers:⎩467⎭
    ⎩468⎭
    1. IP (Instruction Pointer): References the current position within the⎩469⎭
    threaded code array being interpreted. Since threaded words may invoke⎩470⎭
    other threaded words, IP must be preserved in a reentrant manner via⎩471⎭
    the return stack on each invocation.⎩472⎭
    ⎩473⎭
    2. W (Word Pointer): References the CFA of the currently executing primitive.⎩474⎭
    This global register serves an analogous function to 'self' in object-oriented⎩475⎭
    languages, enabling subroutines to access word header fields through fixed⎩476⎭
    offsets from the CFA.⎩477⎭
    ⎩478⎭
    Optimization rationale: W is positioned to reference the CFA rather than the⎩479⎭
    word header base. This design eliminates offset arithmetic for CFA access—the⎩480⎭
    most frequent header operation—at the cost of requiring offset adjustments⎩481⎭
    for other header fields (NFA: W-2, flags: W-1, PFA: W+1). This represents a⎩482⎭
    deliberate trade-off favoring the common case.⎩483⎭
    ⎩484⎭
    The inner interpreter loop performs the following operations:⎩485⎭
    - Fetch the next CFA from RAM[IP] into W (performing the first indirection)⎩486⎭
    - Increment IP to advance through the threaded code array⎩487⎭
    - Execute the primitive via RAM[W]() (performing the second indirection)⎩488⎭
    ⎩489⎭
    By caching the dereferenced CFA in W, we amortize the cost of double⎩490⎭
    indirection: both primitive execution and header field access within⎩491⎭
    subroutines utilize the same cached reference, avoiding redundant⎩492⎭
    dereferences. This is functionally equivalent to parameter passing in⎩493⎭
    object-oriented method invocation, but eliminates the overhead of⎩494⎭
    explicitly passing 'self' to each primitive.⎩495⎭
    ⎩496⎭
    Note: W's state is only defined during primitive execution (within RAM[W]()).⎩497⎭
    Between loop iterations, W may reference a stale CFA, but this is⎩498⎭
    architecturally sound since W is unconditionally updated before each⎩499⎭
    primitive invocation.⎩500⎭
                                                       #line 501#line 502
    State.R.append ( IP)                               #line 503
    IP =  W+ 1                                         #line 504
    while ( -1!= State.RAM [ State.IP]):               #line 505
        W =  State.RAM [ State.IP]                     #line 506
        State.IP =  State.IP+ 1                        #line 507 State.RAM [ State.W]()#line 508#line 509
    IP = State.R.pop ()                                #line 510#line 511#line 512

def xcolon ():
    global State                                       #line 513
    # ( name | --) Start compilation.                  #line 514

    blank =  32                                        #line 515
    State.S.append ( blank)                            #line 516 word()#line 517

    name = State.S.pop ()                              #line 518
    code( name, doword)                                #line 519
    State.compiling = True                             #line 520#line 521#line 522

def xsemi ():
    global State                                       #line 523
    # ( --) Finish definition.                         #line 524
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<   #line 525
    State.RAM.append( -1)
    # Marker for end of definition.                    #line 526
    State.compiling = False                            #line 527#line 528#line 529

def xinterpret ():
    global State                                       #line 530
    # ( string --) Execute word.                       #line 531#line 532 xfind()#line 533

    immediate = State.S.pop ()                         #line 534
    if State.compiling:                                #line 535
        xt = State.S.pop ()                            #line 536
        if  immediate:                                 #line 537
            State.W =  xt                              #line 538
            State.IP =  -1
            # Dummy to hold place in return stack.     #line 539 State.RAM [ xt]()
            # Execute code.                            #line 540
        else:                                          #line 541
            State.RAM.append( xt)                      #line 542#line 543
    else:                                              #line 544
        word = State.S.pop ()                          #line 545
        if (re.match(r"^-?d*$", word)):                #line 546
            State.S.append (int ( word))               #line 547
            if  immediate:                             #line 548 internalize()#line 549#line 550
        elif (re.match(r"^-?d*.?d*$", word)):          #line 551
            State.S.append (float ( word))             #line 552
            if  immediate:                             #line 553 internalize()#line 554#line 555
        else:                                          #line 556

            State.S.clear()                            #line 557

            State.R.clear()                            #line 558
            print ( word, end="")                      #line 559
            print ( "?", end="")                       #line 560
            print ()                                   #line 561
            return  False                              #line 562#line 563#line 564
    return  True                                       #line 565#line 566#line 567
                                                       #line 568#line 569#line 570#line 571
# Example of state-smart word, which Brodie sez not to do. Sorry, Leo... #line 572
# This sin allows it to be used the same way compiling or interactive. #line 573
def xquote ():
    global State                                       #line 574
    # ( -- string) Read up to closing quote, push to stack. #line 575
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<   #line 576
    State.S.append ( 34)                               #line 577 xword()#line 578
    if  1 ==  fvget( "state"):                         #line 579 literalize()#line 580#line 581#line 582#line 583

def xdotquote ():
    global State                                       #line 584
    # ( --) Print string.                              #line 585 xquote()#line 586
    print (State.S.pop (), end="")                     #line 587#line 588#line 589

def xcomment ():
    global State                                       #line 590
    # ( --) Read up to close paren.                    #line 591
    %  >>>  error - unrecognized builtin "immediate" (with given arguments)  <<<   #line 592

    rpar =  41                                         #line 593
    State.S.append ( rpar)                             #line 594 xword()#line 595
    State.S.pop ()                                     #line 596#line 597#line 598
                                                       #line 599
def doliteral ():
    global State                                       #line 600
    # Inside definitions only, pushes compiled literal to stack. #line 601
    State.S.append ( RAM [ IP])
    # Push item at IP on stack.                        #line 602
    State.IP =  State.IP+ 1
    # Advance IP past item to continue execution.      #line 603#line 604#line 605

def literalize ():
    global State                                       #line 606
    # Compile literal into definition.                 #line 607
    RAM.append( _find( "(literal)"))
    # Compile address of doliteral.                    #line 608
    RAM.append(State.S.pop ())
    # Compile literal value.                           #line 609#line 610#line 611
                                                       #line 612
def xinterpret ():
    global State                                       #line 613
    # ( string --) Execute word                        #line 614

    word = State.S.pop ()
    if(  word):                                        #line 618

        found, subr = Lookup (subrs,  word)            #line 619
        if  found:                                     #line 620 subr()#line 621
        elif  word.isdigit():
            State.S.append (int ( word))
        else:                                          #line 625
            print ( word, end="")                      #line 626
            print ( "?", end="")                       #line 627
            print ()                                   #line 628#line 629#line 631#line 632
subrs = {                                              #line 633

    "drop" : xdrop,
    "dup" : xdup,
    "negate" : xnegate,
    "emit" : xemit,
    "cr" : xcr,
    "." : xdot,
    ".s" : xdots,
    "+" : xadd,
    "*" : xmul,
    "swap" : xswap,
    "-" : xsub,
    "/" : xdiv,
    "word" : xword,
}
%  >>>  error - unrecognized builtin "assoc" (with given arguments)  <<<  (subrs,'"',↪︎xquote) #line 647%  >>>  error - unrecognized builtin "assoc" (with given arguments)  <<<  (subrs,'."',↪︎xdotquote) #line 648
subrs ["("] =  xcomment                                #line 649%  >>>  error - unrecognized builtin "assoc" (with given arguments)  <<<  (subrs,"(literal)",doliteral) #line 650
subrs ["branch"] =  xbranch                            #line 651
subrs ["0branch"] =  x0branch                          #line 652
subrs ["if"] =  xif                                    #line 653
subrs ["else"] =  xelse                                #line 654
subrs ["then"] =  xthen                                #line 655
subrs ["constant"] =  xconst                           #line 656
subrs ["create"] =  xcreate                            #line 657
subrs [","] =  xcomma                                  #line 658
subrs ["variable"] =  xvar                             #line 659
subrs ["dump"] =  xdump                                #line 660
subrs ["@"] =  xstore                                  #line 661
subrs ["!"] =  xstore                                  #line 662
subrs ["bye"] =  xbye                                  #line 663
subrs ["find"] =  xfind                                #line 664
subrs ["'"] =  xtick                                   #line 665
subrs ["None"] =  pushNone                             #line 666
subrs ["words"] =  xwords                              #line 667
subrs ["execute"] =  xexecute                          #line 668
subrs [":"] =  xcolon                                  #line 669
subrs [";"] =  xsemi                                   #line 670
subrs ["interpret"] =  xinterpret                      #line 671#line 672
def ok ():
    global State                                       #line 673
    # ( --) Interaction loop -- REPL                   #line 674

    blank =  32                                        #line 675
    while  True:                                       #line 676

        State.BUFF = input("OK ")
        State.BUFP = 0
                                                       #line 677
        while not (State.BUFP >= len(State.BUFF)):     #line 678
            if ( xinterpret()):                        #line 679
                print ( " ok", end="")                 #line 680
                print ()                               #line 681#line 682#line 683#line 684#line 685#line 686
ok()                                                   #line 687#line 688