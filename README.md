# pyRefactor

## python3 refactor tool for multilingual projects

The script produces a file list from a given folder by searching through for all the user-defined file suffixes. This information is then used to analyze and build a database of variables, class names etc. Finally, this database can be fed to the script to do complete project-wise search and replace of those strings. This way one can do all the changes in one go, and easily unify the project variable naming.


## Example


### Create file listing
```python
rdir = '../../corgi'
fs = get_files(rdir, ('.py', '.c++', '.h'))
write_files(fs)
```

Produces `files.txt` (that you can modify as you wish):
```
[py]
../plasmabox/corgi/examples/game-of-life/simulation.py
../plasmabox/corgi/pycorgi/corgi.py
../plasmabox/corgi/tests/test_ca.py

[cpp]
../plasmabox/corgi/cellular_automata.h
../plasmabox/corgi/common.h
../plasmabox/corgi/communication.h
../plasmabox/corgi/corgi.h
```

### Create variable database
```python
#read_variables('cpp', 'files.txt')
read_variables('cpp', 'files.txt', detect_only_camelcase=True)
#read_variables('cpp', 'files.txt', detect_only_underscore=True)
```
This tries to sniff out every variable name longer than 3 characters. Some common language specific keywords are automatically filtered out.

As an example of the output, here we would get:
```
getYmin 
getYmax
CellType
DataContainer
currentStep
_mpiGrid
getTile
getData
CellularAutomataCell
```

### Create database of new names
Next, you can use the `variables.txt` as a basis for creating a list of wanted substitutions (rename this for e.g. into `replace.txt`). The syntax is `old_variable => new_variable` with one replacement per line.

As an example, we could write:
```
getYmin => get_ymin
getYmax => get_ymax
CellType 
DataContainer
currentStep
_mpiGrid
getTile
getData
CellularAutomataCell
```

If no replacement is given (i.e., there is no `=> xxx`), then the line is ignored.

### Substitute
Finally, we can feed the list of replacements into the script that tries its best to replace all those occurrences. The script also prints out lots of statistics of the possible changes.

```python
search_and_replace('files.txt', 'replace.txt')
```

Producing:
```
../plasmabox/corgi/internals.h
../plasmabox/corgi/tags.h
../plasmabox/corgi/tile.h
../plasmabox/corgi/examples/game-of-life/gol.c++
../plasmabox/corgi/examples/game-of-life/gol.h
../plasmabox/corgi/examples/game-of-life/pygol.c++
../plasmabox/corgi/pycorgi/pycorgi.c++
    3 hits (0 new hits)
*********
136: .def("getYmax", [](corgi::Node<1> & ){ return 1.0; });
189: .def("getYmax", [](corgi::Node<2> &n){ return n.getYmax(); });
*********
../plasmabox/corgi/tests/corgitest.c++
../plasmabox/corgi/tests/corgitest.h
../plasmabox/corgi/tests/pycorgitest.c++
../plasmabox/corgi/toolbox/dataContainer.h
../plasmabox/corgi/toolbox/sparse_grid.h
../plasmabox/corgi/toolbox/unstable_remove.h
```
and so on.





