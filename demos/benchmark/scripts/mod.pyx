def benchmark_mod(cont):
	
	own = cont.owner
	
	sensor = cont.sensors[0]
	
	lst = []
	benchmark = int(own['benchmark'])
	
	if sensor.positive:
		own.applyRotation([0, 0, 0.02], True)
		
		for i in range(benchmark):
			lst.append(i)
			
	pass