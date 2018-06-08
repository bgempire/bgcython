import sys
import os
import shutil

from pathlib import Path
from subprocess import call
from pprint import pprint, pformat
from ast import literal_eval

from .utils import *

__all__ = ['bgcythonize']

py_lib_version = 'python' + str(sys.version_info[0]) + str(sys.version_info[1])
cur_path = Path(__file__).parent.resolve()

# Compiler settings
settings = load_settings()

# Paths
path_python = Path(settings['path_python']).resolve()
path_gcc = Path(settings['path_gcc']).resolve()
py_include = Path(settings['py_include']).resolve()
py_libs = Path(settings['py_libs']).resolve()

def bgcythonize(target_path):
	
	""" Converts Python script to C code using Cython, the compile to extension using GCC.

	target_path = Changes will be processed in the given path."""
	
	# Paths
	target_path = Path(target_path).resolve()
	
	# Main data
	mods_to_build = load_timestamps(target_path)
	
	# Continue if all given paths are valid
	if target_path.exists() and path_gcc.exists() and py_include.exists() and py_libs.exists():
		
		# Convert .pyx to .c files
		for _f in mods_to_build:
			
			_file = Path(target_path.as_posix() + '/' + _f).resolve()
			
			cythonize_command = path_python.as_posix() + '/python -m Cython.Build.Cythonize --force --lenient ' + _file.as_posix()
			
			print('Cythonize .pyx file:\n', cythonize_command, '\n')
			call(cythonize_command)
			
		# Compile .c into .o files
		for _f in mods_to_build:
			
			_file = Path(target_path.as_posix() + '/' + _f).resolve().with_suffix('.c')
			
			gcc_command = '"' + path_gcc.as_posix() + '/gcc" -c -I"' + py_include.as_posix() + '" -o "' + _file.with_suffix('.o').as_posix() + '" "' + _file.with_suffix('.c').as_posix() + '"'
			#'gcc -c -IC:\Python36\include -o *.o *.c'
			
			print('Compile .c into .o:\n', gcc_command, '\n')
			call(gcc_command)
			
		# Compile .o into extensions
		for _f in mods_to_build:
			
			_file = Path(target_path.as_posix() + '/' + _f).resolve().with_suffix('.o')
			
			# gcc -shared -LC:/Python36/libs -o *.pyd *.o -lpython36
			gcc_command =  '"' + path_gcc.as_posix() + '/gcc" -shared -L"' + py_libs.as_posix() + '" -o "' + _file.with_suffix('.pyd').as_posix() + '" "' + _file.with_suffix('.o').as_posix() + '" -l' + py_lib_version
			
			print('Compile .o into extension:\n', gcc_command, '\n')
			call(gcc_command)
				
		for _f in mods_to_build:
			
			_file_o = Path(target_path.as_posix() + '/' + _f).resolve().with_suffix('.o')
			_file_c = Path(target_path.as_posix() + '/' + _f).resolve().with_suffix('.c')
			
			if _file_o.exists() and _file_c.exists():
				
				print('Deleting files:\n', _file_o.as_posix(), '\n', _file_c.as_posix(), '\n')
				
				_file_o.unlink()
				_file_c.unlink()
			
		gen_timestamps(target_path)
		
	pass

