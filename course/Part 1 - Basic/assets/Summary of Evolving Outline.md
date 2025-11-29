Claude says: Based on the Discord discussion, here's the outline for the Forthish course that's been discussed:

## Course Structure

**Week 1: Introduction to simple.py**

- Focus exclusively on understanding `simple.py` (the minimal Forth interpreter in ~50 lines of Python)
- Contains fundamental "aha" moments about simplicity for people steeped in modern function-based programming
- **Exercise 1**: Implement a comment parser - something "deadly simple" like parsing `(a b c)` comments
- Expected outcome: Students will likely create over-elaborate solutions, then learn the simple "eat-text-until-you-see-an-rpar" approach, creating new "aha"s
- The goal is to show how much can be understood from this tiny piece of code

**Week 2: Compilation**

- Introduce the compiler variant (likely `fcomp.py`)
- Demonstrate that "compilation" can be trivial too
- Show quantum leaps between different file versions

**Future Weeks**

- Continue implementing Moore's 27(?) Machine Forth primitives, one by one
- Explore how Forth can change parser behavior from the environment (a key advantage over static parsers)

## Format Questions Still Being Discussed

- Whether it's actually weekly or do-at-your-own-speed-and-ask-questions-along-the-way
- Need for a "start here, follow this plan" channel
- Consideration of using platforms like Leanpub to build a formal "course"

The discussion was still evolving, with plans to announce at the next Torlisp meeting (Oct 14th).