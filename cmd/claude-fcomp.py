APP = dict(
    name="Forth Compiling",
    about="Forth that reads from stdin instead of implementing its own REPL",
    fork="Based on ../basic/comp/fcomp.py"
)

import re
import sys
import json
import os

S = None
R = None
RAM = None
LAST = None
IP = None
BUFF = None
BUFP = None
St = None

class Stack(list):
    def push(my, *items):
        my.extend(items)

class State:
    def __init__(self):
        self.S = Stack() 
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None
        self.BUFF = ""
        self.BUFP = 0
        self.function_registry = {}
    
    def register_function(self, func):
        """Register a function so it can be serialized/deserialized"""
        self.function_registry[func.__name__] = func
    
    def serialize_item(self, item):
        """Convert an item to JSON-serializable format"""
        if callable(item):
            if hasattr(item, '__name__'):
                return {'__type__': 'function', '__name__': item.__name__}
            else:
                return {'__type__': 'function', '__name__': '<lambda>'}
        elif isinstance(item, list):
            return [self.serialize_item(x) for x in item]
        elif isinstance(item, dict):
            return {k: self.serialize_item(v) for k, v in item.items()}
        else:
            return item
    
    def deserialize_item(self, item):
        """Convert from JSON format back to Python objects"""
        if isinstance(item, dict) and item.get('__type__') == 'function':
            func_name = item['__name__']
            if func_name in self.function_registry:
                return self.function_registry[func_name]
            else:
                print(f"Warning: function '{func_name}' not found in registry")
                return None
        elif isinstance(item, list):
            return [self.deserialize_item(x) for x in item]
        elif isinstance(item, dict):
            return {k: self.deserialize_item(v) for k, v in item.items()}
        else:
            return item
    
    def to_json(self, filename):
        data = {
            'S': [self.serialize_item(item) for item in self.S],
            'R': [self.serialize_item(item) for item in self.R],
            'RAM': [self.serialize_item(item) for item in self.RAM],
            'LAST': self.LAST,
            'IP': self.serialize_item(self.IP),
            'W': self.serialize_item(self.W),
            'BUFF': self.BUFF,
            'BUFP': self.BUFP
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        state = cls()
        # Don't deserialize yet - just store the raw JSON data
        # Deserialization will happen later after functions are registered
        state.S.extend(data['S'])
        state.R.extend(data['R'])
        state.RAM = data['RAM']  # Keep as raw JSON data
        state.LAST = data['LAST']
        state.IP = data['IP']
        state.W = data['W']
        state.BUFF = data['BUFF']
        state.BUFP = data['BUFP']
        
        return state

def code(name, does, flags=0):
    "( name does /flags/ --) Add new word to RAM dictionary."
    global LAST, St
    x = len(RAM)       # This is "HERE".
    RAM.append(LAST)   # Link field.
    RAM.append(name)   # Word name.
    RAM.append(flags)  # Flags
    RAM.append(does)   # Code pointer.
    LAST = x
    
    # Register the function if it's callable
    if St is not None and callable(does):
        St.register_function(does)


    
def xswap(): "( a b -- b a)"; x = S[-1]; S[-1] = S[-2]; S[-2] = x
def xsub():  "(a b -- diff)"; xswap(); S.append(S.pop() - S.pop())
def xdiv():  "(a b -- div)"; xswap(); S.append(S.pop() / S.pop())

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

# Example of state-smart word, which Brodie sez not to do. Sorry, Leo...
# This sin allows it to be used the same way compiling or interactive.
def xquote():
    "( -- string) Read up to closing quote, push to stack."
    S.push(34); xword()
    if 1 == fvget("state"): literalize()

def xdotquote(): "( --) Print string."; xquote(); print(S.pop(), end="")

def xcomment(): "( --) Read up to close paren."; S.push(41); xword(); S.pop()

def doliteral():  # Inside definitions only, pushes compiled literal to stack.
    global IP
    S.push(RAM[IP])  # Push item at IP on stack.
    IP += 1          # Advance IP past item to continue execution.
def literalize():
    "Compile literal into definition."
    RAM.append(_find("(literal)"))  # Compile address of doliteral.
    RAM.append(S.pop())             # Compile literal value.

def xbranch():
    "Inside definitions, jump to address in next cell."
    global IP
    IP = RAM[IP]  # Move IP to address in cell.
def x0branch():
    "Inside definitions, jump to address in next cell, if false."
    global IP
    if bool(S.pop()):
        IP += 1  # Skip over to continue.
    else:
        IP = RAM[IP]  # Move IP to address in cell.

def xif():
    "( f --) Eval if flag is true."
    RAM.append(_find("0branch"))
    R.push(len(RAM))  # Push next address to be updated on else or then.
    RAM.append(-1)    # Placeholder for target jump.
def xelse():
    "( --) Begin opposite clause."
    hanging = R.pop()            # Get "if" slot waiting for address.
    RAM.append(_find("branch"))  # Compile in unconditional branch.
    R.push(len(RAM))             # Push next address to be updated on then.
    RAM.append(-1)               # Placeholder for target jump.
    RAM[hanging] = len(RAM)      # Update "if" slot with next address.
def xthen():
    "( --) Close out if/else/then clause."
    RAM[R.pop()] = len(RAM)

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


def make_push_slot(slot):
    """Factory function to create a push_slot function with a specific slot value."""
    def push_slot():
        S.push(slot)
    push_slot.__name__ = f"push_slot_{slot}"
    return push_slot

def dopushslot():
    """Push the slot value that follows the code pointer in RAM."""
    S.push(RAM[W + 1])

def create(name):
    "( name --) Add name to dictionary."
    slot = len(RAM) + 4  # Address immediately following CODE slot.
    code(name, dopushslot)
    RAM.append(slot)  # Store the slot value after the code pointer

def xcreate():
    "( name | --) Add to dictionary."
    S.push(32); xword(); create(S.pop())


def comma(value): "( value --) Append to dictionary."; RAM.append(value)
def var(name, value):
    "( name value --) Add variable to dictionary."
    create(name)
    comma(value)
def xvar():
    "( name | value --) Add variable to dictionary."
    S.append(32); xword()
    var(S.pop(), S.pop())

def xdump():
    "( start n --) Dump RAM."
    n = int(S.pop())
    start = int(S.pop())
    print("-"*64)
    for a in range(start, start + min(n, (len(RAM) - start))):
        print(f"{a:04}: {RAM[a]}")

def xstore(): "( n a --) Store n at a."; a = S.pop(); RAM[a] = S.pop()

def xbye(): "( --) Leave interpreter."; raise SystemExit

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

def xtick():
    "( name -- xt|-1) Search for execution token of word name."
    S.append(32); xword()
    S.push(_find(S.pop()))


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

def xexecute():
    "( xt --) Execute xt address."
    try:
        # S.append(S[-1]); S.append(6); xdump()  # Debug.
        RAM[S.pop()]()
    except IndexError:
        print("Stack empty!")

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
def xsemi():
    "( --) Finish definition."
    RAM.append(-1)  # Marker for end of definition.
    fvset("state", 0)

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
        # Skip empty words
        if word == "":
            return True
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


# New explicit functions to replace lambdas
def xdrop(): "( a --) Drop TOS."; S.pop()
def xdup(): "( a -- a a) Duplicate TOS."; S.push(S[-1])
def xnegate(): "( n -- -n)"; S.append(-S.pop())
def xemit(): "( n --) Emit specified character."; print(chr(int(S.pop())), end="")
def xcr(): "( --) Print carriage return."; print("")
def xdot(): "( n --) Print TOS."; print(f"{S.pop()} ", end="")
def xdots(): "( --) Print stack."; print(S)
def xadd(): "( a b -- sum)"; S.append(S.pop() + S.pop())
def xmul(): "( a b -- product)"; S.append(S.pop() * S.pop())
def xcomma(): "( value --) Append to dictionary."; comma(S.pop())
def xfetch(): "( a -- n) Fetch value at address."; S.append(RAM[S.pop()])
def xnone(): "( -- None) Push Python None on stack."; S.append(None)


def initialize_code():
    var("state", 0)  # 0 = interpret, 1 = compile
    const("pi", 3.14159)
    code("drop", xdrop)
    code("dup", xdup)
    code("negate", xnegate)
    code("emit", xemit)
    code("cr", xcr)
    code(".", xdot)
    code(".s", xdots)
    code("+", xadd)
    code("*", xmul)
    code("swap", xswap)
    code("-",    xsub)
    code("/",    xdiv)
    code("word", xword)
    code('"', xquote, 1)
    code('."', xdotquote)
    code("(", xcomment, 1)
    code("(literal)", doliteral)
    code("branch", xbranch)
    code("0branch", x0branch)
    code("if", xif, 1)
    code("else", xelse, 1)
    code("then", xthen, 1)
    code("constant", xconst)
    code("create", xcreate)
    code(",", xcomma)
    code("variable", xvar)
    code("dump", xdump)
    code("@", xfetch)
    code("!", xstore)
    code("bye",  xbye)
    code("find", xfind)
    code("'", xtick)
    code("None", xnone)
    code("words", xwords)    
    code("execute", xexecute)
    code(":", xcolon)
    code(";", xsemi, 1)
    code("interpret", xinterpret)

def initialize_globals(state_filename):
    global S, R, RAM, LAST, IP, BUFF, BUFP, St
    
    # Try to load existing state
    if os.path.exists(state_filename):
        try:
            St = State.from_json(state_filename)
            # Restore globals from loaded state
            S = St.S
            R = St.R
            RAM = St.RAM
            LAST = St.LAST
            IP = St.IP
            BUFF = St.BUFF
            BUFP = St.BUFP
            return St
        except Exception as e:
            print(f"Warning: Could not load state from {state_filename}: {e}")
            print("Starting with fresh state...")
    
    # Create fresh state if file doesn't exist or loading failed
    St = State()
    S = St.S
    R = St.R
    RAM = St.RAM
    LAST = St.LAST
    IP = St.IP
    BUFF = ""
    BUFP = 0
    return St



def main():
    global BUFF, BUFP, S, R, RAM, LAST, IP
    
    state_filename = sys.argv[1] if len(sys.argv) > 1 else "state.json"
    
    # Check if we're loading existing state
    loading_state = os.path.exists(state_filename)
    
    # Load or initialize state
    St = initialize_globals(state_filename)
    
    # Save the loaded raw data before initialize_code
    loaded_ram = None
    loaded_s = None
    loaded_r = None
    loaded_last = None
    if loading_state and len(RAM) > 0:
        loaded_ram = RAM.copy()
        loaded_s = list(S)
        loaded_r = list(R)
        loaded_last = LAST
    
    # Always initialize code to register all functions
    # This creates a fresh dictionary
    initialize_code()
    
    # If we loaded state, restore it now that functions are registered
    if loaded_ram is not None:
        # Clear the fresh state
        RAM.clear()
        S.clear()
        R.clear()
        
        # Now deserialize with registered functions available
        for item in loaded_ram:
            RAM.append(St.deserialize_item(item))
        for item in loaded_s:
            S.append(St.deserialize_item(item))
        for item in loaded_r:
            R.append(St.deserialize_item(item))
        
        LAST = loaded_last
        St.RAM = RAM
        St.S = S
        St.R = R
        St.LAST = LAST
    
    # Read lines from stdin
    for line in sys.stdin:
        # Remove trailing newline
        line = line.rstrip('\n')
        # Assign BUFF to the line
        BUFF = line
        St.BUFF = BUFF
        ok = True  # Are things, indeed, ok?
        BUFP = 0
        St.BUFP = BUFP
        while ok and BUFP < len(BUFF):
            ok = xinterpret()
        # Update state with current values
        St.BUFP = BUFP
    
    # Save state before exiting
    St.S = S
    St.R = R
    St.RAM = RAM
    St.LAST = LAST
    St.IP = IP
    St.to_json(state_filename)
    print("")

if __name__ == "__main__":
    main()
