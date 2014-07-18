pycount
=======

* experimental SLOC tool
* doing this for python learning purposes and general OO practicing as I'm a newbie
* feel free to raise issues if you find something unusual (the likelyhood of someone even looking at this is
very close to zero, so I'm not expecting anything :D)

**TODO**
* add rules to separate comments based on type of file
* improve speed, always
* write tests

**INSTALL**
```
pip install pycount
```

**USAGE**

You can run the command at any location in your command line
```
<your code dir>$ pycount
```

Or you can pass it an path argument
```
$ pycount ~/My/Repos/Some/Project
```

Alternatively, you can use the Counter class
```
from pycount.pycount import Counter

COUNTER = Counter() # or Counter('some/path')
COUNTER.discover() # discovers all unique files for a path
COUNTER.count() # counts all lines of code, using the pre-defined file types which should be considered
COUNTER.report() # write the report
```

to see just the files, results, you can use the class attributes
```
COUNTER.discover()
COUNTER.files # lists all the files

COUNTER.count()
COUNTER.results # outputs the dictionary with all the values that were collected through counting
```
