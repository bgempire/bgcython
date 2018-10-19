''' This file is a bgcython standard for use with BGE. This __init__.py file specifies if 
project is a release or is in development. 

- Setting release to False means that project is in development, and bgcython will rebuild 
C extension modules.

- When releasing the project to public, set release to True, as the user will not have the 
same environment to build the C extension modules. '''

### Set this value according to project release process (release/development) ###
release = False

if not release:
	
	from bge.logic import expandPath
	from pathlib import Path
	from bgcython import bgcythonize
	
	current_path = Path(expandPath('//')).resolve()
	
	bgcythonize(current_path)