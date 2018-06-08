import bge
import bgcython

from ast import literal_eval
from pathlib import Path

current_path = Path(bge.logic.expandPath('//')).resolve()

bgcython.bgcythonize(current_path)

def main(cont):

	try:
		from .mod import benchmark_mod

	except:
		print('Cant import extension mod')
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	lst = []
	benchmark = literal_eval(own['benchmark'])
	
	if sensor.positive:
		
		if 'benchmark_mod' in dir() and own['use_mod']:
			print('Running benchmark_mod')
			benchmark_mod(cont)
			
		else:
			benchmark_script(cont)

def benchmark_script(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	lst = []
	benchmark = literal_eval(own['benchmark'])
	
	if sensor.positive:
		
		print('Running benchmark_script')
		
		own.applyRotation([0, 0, 0.02], True)
		
		for i in range(benchmark):
			lst.append(i)