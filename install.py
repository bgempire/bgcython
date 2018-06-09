import sys
import os
import shutil

from pathlib import Path
from subprocess import call
from platform import system

def main(cont):
	
	# Sensors
	sensor = cont.sensors[0]
	
	if sensor.positive:
	
		# Other
		ext_exe = '.exe' if system() == 'Windows' else ''
		system_supported = system() in ['Windows', 'Linux']

		# Paths
		path_current = Path('.').resolve()
		path_getpip = Path(Path(__file__).resolve().parent.as_posix() + '/get-pip.py').resolve()
		path_bgcython = Path(Path(__file__).resolve().parent.as_posix() + '/bgcython').resolve()
		path_blender = Path(sys.executable).resolve()
		path_python = None
		path_sitepkg = None
		
		# Set remaining path variables, walking through blender files structure
		for _path, _folders, _files in os.walk(path_blender.parent.as_posix()):
			
			# python/bin folder
			if _path.endswith('bin'):
				for _file in _files:
					
					_p = Path(_path + '/' + _file).resolve()
					
					# Check if file is a python executable
					if _file.startswith('python') and _file.endswith(ext_exe) and os.access(_p.as_posix(), os.X_OK):
						path_python = _p
			
			# Get folder site-packages from python library
			if _path.endswith('site-packages'):
				path_sitepkg = Path(_path).resolve()
				
			# Break loop to avoid reading unecessary files
			if path_python and path_sitepkg:
				break
		
		### START ###
		### Only continue if all paths exists ###
		if system_supported and path_getpip.exists() and path_bgcython.exists() and path_blender.exists() and path_python.exists() and path_sitepkg.exists():
			
			# Change working directory to Python binaries directory
			os.chdir(path_python.parent.as_posix())
			
			# Print main paths
			print('\n> Blender path is:\n' + path_blender.as_posix() + '\n' +
				'\n> Python path is:\n' + path_python.as_posix() + '\n' +
				'\n> site-packages path is:\n' + path_sitepkg.as_posix() + '\n')
				
			# If pip is not installed
			if not 'pip' in os.listdir(path_sitepkg.as_posix()):
				
				print('pip is not installed, installing it through get-pip.py\n')
				
				# Copy get-pip.py to Python bin folder
				print('Copy get-pip.py to Python bin folder')
				
				shutil.copyfile(
					path_getpip.as_posix(),
					path_python.parent.as_posix() + '/get-pip.py'
					)
					
				# Execute get-pip.py
				print('Execute get-pip.py')
				call(path_python.name + ' get-pip.py')
				
				# Delete get-pip.py
				print('Delete get-pip.py')
				Path(path_python.parent.as_posix() + '/get-pip.py').resolve().unlink()
				
				print('pip successfully installed\n')
			
			# Continue if pip is installed
			if 'pip' in os.listdir(path_sitepkg.as_posix()):
				
				# If Cython is not installed
				if not 'Cython' in os.listdir(path_sitepkg.as_posix()):
					
					print('Cython is not installed, installing it through pip\n')
					
					# Install Cython through pip
					call(path_python.name + ' -m pip install Cython')
					
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
						
					# Copy settings.txt to package folder
					print('Copying settings.txt package folder')
					
					shutil.copyfile(
						path_bgcython.as_posix() + '/settings.txt',
						path_sitepkg.as_posix() + '/bgcython/settings.txt'
						)
						
					print('bgcython successfully installed\n')
					
					# Open settings file for editing
					os.startfile(path_sitepkg.as_posix() + '/bgcython/settings.txt')
					
			print('Installation successfully ended')
					
		# Change working directory back to current 
		os.chdir(path_current.as_posix())