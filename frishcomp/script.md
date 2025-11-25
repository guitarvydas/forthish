













# Interpret ()

## Words

Words are like stunted OO objects that have exactly one method.

The method is referred to by the CFA field

CFA stands for Code Field Address.

Every Word has a CFA. 

A word can have a PFA - Parameter Field Address. A bunch of raw bytes immediately following the word.

The CFA always points to native code.
- CFA for a native code word points to a native subroutine, e.g. xadd()
- CFA for threaded code word points to the subroutine *doword()* which sequentially runs every function in the PFA array
## Outer Interpreter
Executes Words at the top level by invoking a word's "CFA" subroutine.
## Inner Interpreter
- nested Words

## Interpreting code
```
: double 2 * ;
: quad double double ;
7 quad .
```
## Already compiled:
```
: double 2 * ;
: quad double double ;
```  

## In the process of interpreting
```
7 quad .
```

## Already interpreted
```
7 
```
which leaves 7 on the data stack.

---






















































# System State At This Point...

### 5 Words (Forth “objects”) in red

### Threaded code (addresses of words) in yellow
  _“address” is shorthand for “index into array of memory cells (aka RAM)”_

### data stack

### return stack

### registers: W, IP
- W is “word”
	- green dot
- IP is “instruction pointer”
	- blue dot

- W is like self - a global variable instead of being passed explicitly as a parameter

### Actual layout is an array of memory cells 
RAM --> Random Access Memory

Diagram is compressed and abstracted to make this presentation less cluttered. 
- Native code elided
- input BUFFer elided

---

# Step 1

## call xfind() 
#### figure out XT of the word to be interpreted 

#### is the word "normal"?
- 0
- word is simply inlined during compilation
#### is the word "immediate"?
- 1
- word executes during compilatin

#### xfind returns 2 items on data stack
- top = immediate (1 or 0)
- 2nd = XT = index of indirect pointer to code (CFA of target word object)

## set W to XT (89)
- offsets from W give access to other fields of word
- e.g. (W - 2) = name

## set IP to -1

## call code indirectly through W
- W is a pointer to a CFA (Code Field Address) cell that contains a pointer to executable code instead of just an integer
- In assembler Forth, pointer == integer
- In higher level languages pointer == *typed* integer
---

# Step 2
CFA contains pointer to ‘doword()' (indirect through cell 89)
doword() will sequentially walk through list of subroutines
doword begins by saving IP on the Return Stack ... push -1
IP is made to point to the front of the list of subroutines,
in this case W + 1 (89 + 1 = 90)

read address in IP -> RAM[90] -> 72 and set W=72

call subroutine pointed to by W -> doword ()

---

# Step 3
save IP on the Return Stack
IP is made to point to the front of the list of subroutines,
in this case W + 1 (72 + 1 = 73)

read address in IP -> RAM[73] -> 51 and set W=51

call subroutine pointed to by W -> doliteral ()

---

# Step 4
doliteral parses immediate value next in threaded list, i.e. 2
push 2 onto data stack

perform NEXT - pop Return Stack into IP

---
