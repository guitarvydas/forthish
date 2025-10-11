# Install mercurial
## bash
`$ sudo apt install mercurial`
## macOS (with homebrew)
`$ brew install mercurial`
# Clone Forthish
`$ mkdir forthish`
`$ cd forthish`
`$ hg clone https://hg.sr.ht/~oofoe/forthish`

# Proceed
begin by looking at `simple.py` and trying it out
`python3 simple.py`
```
$ python3 simple.py 
OK 1
OK .s
[1]
OK 2
OK .s
[1, 2]
OK +
OK .s
[3]
OK
```
Read README.md.

# Future Pulls
After installing, you can pull that latest versions with
`hg pull -u`
