(open `./fram.svg` in a browser)
![fram.y](./fram.svg)

I'll create a visual diagram showing how the RAM dictionary structure works in fram.py.This diagram illustrates the key architectural features of fram.py:

**RAM Dictionary Structure:**

- Each word occupies 3 consecutive cells: name, link, code
- Links form a backward-pointing chain (newest words first)
- RAM_NEXT always points to the most recently defined word

**Search Algorithm:**

- Starts at RAM_NEXT and follows links backward
- First match wins (allowing word redefinition/shadowing)
- Returns execution token (address + 2) pointing to code

**Key Insight:** This implements the classic Forth dictionary as a **linked list in linear memory** - a simple but powerful design that enables:

- Runtime word definition
- Word redefinition (shadowing)
- Dictionary introspection (`words` command)
- Indirect execution (`'` and `execute`)

The beauty is in its simplicity - just a few data structures implementing a surprisingly powerful and extensible language system!