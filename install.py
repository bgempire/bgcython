import sys
import os
import shutil

from pprint import pprint
from pathlib import Path
from subprocess import call
from platform import system

def main():

	# Paths
	path_current = Path('.').resolve()
	path_getpip = Path(Path(__file__).resolve().parent.as_posix() + '/get-pip.py').resolve()
	path_bgcython = Path(Path(__file__).resolve().parent.as_posix() + '/bgcython').resolve()
	path_blender = None
	path_python = None
	path_sitepkg = None

	# Other
	ext_exe = '' if system() != 'Windows' else '.exe'
	
	# Set some path variables
	for _path in sys.path:
		
		if _path.endswith('python'):
			path_python = Path(_path + '/bin').resolve()
		
		if _path.endswith('site-packages'):
			path_sitepkg = Path(_path).resolve()
			
	
	path_blender = path_python.parent.parent.parent
			
	if path_blender and path_python and path_sitepkg:
		
		# Change working directory to Python binaries directory
		os.chdir(path_python.as_posix())
		
		print(
			'\nBlender path is:\n', path_blender.as_posix() + '\n',
			'\nPython path is:\n', path_python.as_posix() + '\n',
			'\nsite-packages path is:\n', path_sitepkg.as_posix() + '\n'
			)
			
		# If pip is not installed
		if not 'pip' in os.listdir(path_sitepkg.as_posix()):
			
			print('pip is not installed, installing it through get-pip.py\n')
			
			# Copy get-pip.py to Python bin folder
			print('Copy get-pip.py to Python bin folder')
			
			shutil.copyfile(
				path_getpip.as_posix(),
				path_python.as_posix() + '/get-pip.py'
				)
				
			# Execute get-pip.py
			print('Execute get-pip.py')
			call('python get-pip.py')
			
			# Delete get-pip.py
			print('Delete get-pip.py')
			Path(path_python.as_posix() + '/get-pip.py').resolve().unlink()
			
			print('pip successfully installed\n')
		
		# Continue if pip is installed
		if 'pip' in os.listdir(path_sitepkg.as_posix()):
			
			print('pip is installed, continuing\n')
			
			# If Cython is not installed
			if not 'Cython' in os.listdir(path_sitepkg.as_posix()):
				
				print('Cython is not installed, installing it through pip\n')
				
				# Install Cython through pip
				call('python -m pip install Cython')
				
				print('Cython successfully installed\n')
			
			# If bgcython is not installed
			if not 'bgcython' in os.listdir(path_sitepkg.as_posix()):
				
				print('bgcython is not installed, installing it\n')
				
				# Copy bgcython package to site-packages
				print('Copying bgcython package to site-packages')
				
				shutil.copytree(
					path_bgcython.as_posix(),
					path_sitepkg.as_posix() + '/bgcython/'
					)
					
				# Copy settings_bgcython.txt package folder
				print('Copying settings_bgcython.txt package folder')
				
				shutil.copyfile(
					path_bgcython.as_posix() + '/settings_bgcython.txt',
					path_sitepkg.as_posix() + '/bgcython/settings_bgcython.txt'
					)
					
				print('bgcython successfully installed\n')
				
				# Open settings file for editing
				os.startfile(path_sitepkg.as_posix() + '/bgcython/settings_bgcython.txt')
				
	# Change working directory back to current 
	os.chdir(path_current.as_posix())