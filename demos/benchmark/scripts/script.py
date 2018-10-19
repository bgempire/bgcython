def main(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	lst = []
	benchmark = int(own['benchmark'])
	
	if sensor.positive:
		
		# Allowed to use mod
		if own['use_mod']:
			
			# Import mod if not already imported
			if not 'benchmark_mod' in dir(): 
				
				try:
					from .mod import benchmark_mod

				except:
					print('Cant import extension mod function')
					
			print('Running function benchmark_mod')
			benchmark_mod(cont)
			
		# Not allowed to use mod
		elif not own['use_mod']:
			
			# Delete mod if it is imported
			if 'benchmark_mod' in dir():
				del benchmark_mod
				
			benchmark_script(cont)

def benchmark_script(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	lst = []
	benchmark = int(own['benchmark'])
	
	if sensor.positive:
		
		print('Running function benchmark_script')
		
		own.applyRotation([0, 0, 0.02], True)
		
		for i in range(benchmark):
			lst.append(i)