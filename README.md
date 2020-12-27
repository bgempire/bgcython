# BGCython #

BGCython is a [Cython](http://cython.org/) implementation for 
[BGE](https://en.wikipedia.org/wiki/Blender_Game_Engine), building extensions 
automatically at GE start whenever the source files are modified. It only needs 
a single line of code to compile all of your `.pyx` files in the given path into 
C extensions.

## Install ##

Clone / download the repository and run the blend file named `install.blend`. 
The blend contains some instructions, the most important being to enable the 
Blender console to check the progress of installation and other messages.

This blend will run the script `install.py`, that will run `ensurepip` (to 
install [pip](https://pypi.org/project/pip/) on your Blender), then it will 
install [Cython](http://cython.org/) through [pip](https://pypi.org/project/pip/) 
and will copy package files into your Blender's Python library.

After the installation, a settings text file called `settings.txt` will/may 
run, and you can fill some fields with some custom paths if you want.

### Windows ###

Now, you must get the [GCC](https://gcc.gnu.org/) compiler. In case you're 
using Windows, download and install [MinGW](https://sourceforge.net/projects/mingw/) 
through the web installer, and select only The GNU C++ Compiler to install. 
After the installation, the default installation path may be `C:\MinGW`. I recommend you 
to [add C:\MinGW\bin to your system path](https://www.java.com/en/download/help/path.xml) 
to easily run it through command line. After you do that, run in the command prompt:

`gcc --version`

And if the result is something like:

```
gcc (MinGW.org GCC-6.3.0-1) 6.3.0
Copyright (C) 2016 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

You're done. However, you can only add the path `C:/MinGW/bin` to 
`settings.txt`, on `path_gcc` value, like this:

`'path_gcc' : 'C:/MinGW/bin'`

And BGCython will be able to find it.

### Linux ###

TODO

## Using ##

Check the demo `demos/benchmark/benchmark.blend` to test the module. You may need 
to modify `scripts/mod.pyx` to make BGCython recreate the timestamps and compile 
the `.pyx` file, but it must do it, otherwise the installation may not have worked.

To use BGCython, all you need to do is call inside a initialization script 
(preferably in module level) the function:

```python
bgcython.bgcythonize(current_path)
```

The recommended standard is a `__init__.py` on the top level of your scripts 
folder with the following code:

```python
# Set to True on game release
release = False

if not release:
	
	from bge.logic import expandPath
	from pathlib import Path
	from bgcython import bgcythonize
	
	current_path = Path(expandPath('//')).resolve()
	
	bgcythonize(current_path)
```

With `current_path` being the path you want the module to look for `.pyx` scripts. 
It will look recursively on all folders on thegiven path, and create a `timestamps.txt` 
file on this path. After this first run, everytime you modify your `.pyx` files and
run BGE, BGCython will rebuild the extensions. See the demos on this repository for 
further advice.

The `.pyx` files and `timestamps.txt` can be discarded on your release, you only 
need the compiled extensions.
