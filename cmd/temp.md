I've attached the raw python code before adding serialization. 
It is a simplified Forth interpreter.
At the beginning of main, I want restore the state of the interpreter from file 'stateFileName'.
At the end of main, I want to save the state of the interpreter to the file 'stateFileName'.
I haven't decided what to do about the edge case of the first time around, when the state should be empty.





Stack is currently defined as
```
class Stack(list):
    def push(my, *items):
        my.extend(items)
```


```
class State:
    def __init__ (self):
        self.S = Stack() 
        self.R = Stack()
        self.RAM = []
        self.LAST = -1
        self.IP = None
        self.W = None;
        self.BUFF = ""
        self.BUFP = 0
    def to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
    
    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return cls(**data)

...

Traceback (most recent call last):
  File "/Users/paultarvydas/projects/forthish-git/cmd/fcomp.py", line 367, in <module>
    main()
    ~~~~^^
  File "/Users/paultarvydas/projects/forthish-git/cmd/fcomp.py", line 364, in main
    St.to_json (stateFileName)
    ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/Users/paultarvydas/projects/forthish-git/cmd/fcomp.py", line 33, in to_json
    json.dump(self.__dict__, f, indent=2)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/__init__.py", line 179, in dump
    for chunk in iterable:
                 ^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/encoder.py", line 433, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/encoder.py", line 407, in _iterencode_dict
    yield from chunks
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/encoder.py", line 440, in _iterencode
    o = _default(o)
  File "/opt/homebrew/Cellar/python@3.13/3.13.5/Frameworks/Python.framework/Versions/3.13/lib/python3.13/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type function is not JSON serializable
```
