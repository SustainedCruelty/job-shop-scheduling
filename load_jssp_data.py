from typing import List, Tuple
def load_jssp_data(file_path: str) -> Tuple[int, int, List[List[Tuple[int, int]]]]:
	with open(file_path, 'r') as f:
		lines = f.readlines()
		
	# Remove comments and empty lines
	lines = [line for line in lines if not line.startswith('#') and line.strip()]
	
	# First line gives the number of jobs and machines
	num_jobs, num_machines = map(int, lines[0].strip().split())
	
	# Remaining lines give the operations for each job
	jobs = []
	for line in lines[1:]:
		operations = list(map(int, line.strip().split()))
		jobs.append([(operations[i], operations[i+1]) for i in range(0, len(operations), 2)])
	
	return num_jobs, num_machines, jobs