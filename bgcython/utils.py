import sys
import os
import shutil

from pathlib import Path
from pprint import pprint, pformat
from ast import literal_eval

__all__ = ['load_settings', 'gen_timestamps', 'load_timestamps']

python_version = 'python' + str(sys.version_info[0]) + str(sys.version_info[1])
cur_path = Path(__file__).parent.resolve()

def load_settings():
	
	""" Loads bgcython settings for later use, like gcc path, Python includes and libs. """
	
	_settings = {}
	
	# Load settings from file in Blender executable folder
	with open(cur_path.as_posix() + '/settings.txt', 'r') as opened_file:
		_settings = literal_eval(opened_file.read())

	# Get gcc from path if no path is provided
	if _settings['path_gcc'] == '':
		_settings['path_gcc'] = Path(shutil.which('gcc')).resolve().parent

	# Use default include if no path is provided
	if _settings['py_include'] == '':
		_settings['py_include'] = Path(Path(__file__).resolve().parent.as_posix() + '/resources/' + python_version + '/include').resolve()

	# Use default libs if no path is provided
	if _settings['py_libs'] == '':
		_settings['py_libs'] = Path(Path(__file__).resolve().parent.as_posix() + '/resources/' + python_version + '/libs').resolve()
	
	for _path in sys.path:
		if _path.endswith('python'):
			_settings['path_python'] = Path(_path + '/bin').resolve()
			
			break
			
	return _settings
	
def gen_timestamps(target_path):
	
	""" Get and generates timestamps file on given path.
	
	This function is used by load_timestamps.  """
	
	# Paths
	target_path = Path(target_path).resolve()
	timestamps_path = Path(target_path.as_posix() + '/timestamps.txt')
	
	# Main data
	timestamps = {}
	
	# Other
	pyx_files_exist = False
	first_time_build = False
	
	# Get directory of target_path, if not already is one
	if not target_path.is_dir():
		target_path = target_path.parent
		
	# Create timestamps.txt at target_path, if not already exists
	if not timestamps_path.exists():
		print('timestamps.txt doesnt exist, creating it')
		timestamps_path.touch()
		timestamps_path = timestamps_path.resolve()
		first_time_build = True
		
	# Iterates over all files in target_path recursively
	for _path, _folders, _files in os.walk(target_path.as_posix()):
		
		# Iterates over _files in current iteration _path
		for _file in _files:
			
			# Only add .pyx to timestamps
			if _file.endswith('.pyx'):
				
				# Sign that a .pyx file was found
				pyx_files_exist = True
				
				_file_path = Path(_path + '/' + _file).resolve()
				
				# key_name is a relative path from target_path to _file
				key_name = Path(_path).resolve().as_posix().replace(target_path.as_posix(), '') + '/' + _file
				
				# Assign key_name to file modification time value
				timestamps[key_name] = os.path.getmtime(_file_path.as_posix())
	
	# Save timestamps.txt if any .pyx file was found
	if pyx_files_exist:
		
		with open(timestamps_path.as_posix(), 'w') as opened_file:
			
			opened_file.write(pformat(timestamps))
			print('.pyx files timestamps updated to timestamps.txt')
			
	# Warn that no .pyx files were found
	if not pyx_files_exist:
		print('No .pyx files in given path:\n' + target_path.as_posix())
		
	# Timestamps were saved to file, but can be retrieved as function return
	return([timestamps], first_time_build)

def load_timestamps(target_path):
	
	# Paths
	target_path = Path(target_path).resolve()
	timestamps_path = Path(target_path.as_posix() + '/timestamps.txt')
	
	# Main data
	first_time_build = False
	timestamps = {}
	timestamps_mod = []
	
	# Get directory of target_path, if not already is one
	if not target_path.is_dir():
		target_path = target_path.parent
		
	# Generate timestamps.txt at target_path, if not already exists
	if not timestamps_path.exists():
		first_time_build = gen_timestamps(target_path)[1]
		
	# Load timestamps.txt if they exist
	if timestamps_path.exists():
		
		with open(timestamps_path.as_posix(), 'r') as opened_file:
			timestamps = literal_eval(opened_file.read())
		
		if not first_time_build:
			
			for _path, _folders, _files in os.walk(target_path.as_posix()):
				
				for _file in _files:
					if _file.endswith('.pyx'):
						
						pyx_files_exist = True
						
						_file_path = Path(_path + '/' + _file).resolve()
						
						key_name = Path(_path).resolve().as_posix().replace(target_path.as_posix(), '') + '/' + _file
						
						if key_name in timestamps.keys():
							
							if os.path.getmtime(_file_path.as_posix()) == timestamps[key_name]:
								print('No modifications on:', key_name, '\n')
								
							else:
								print('Modified, must recompile:', key_name, '\n')
								timestamps_mod.append(key_name)
							
			return(timestamps_mod)
			
		if first_time_build:
			return(timestamps)