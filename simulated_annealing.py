import random
import math
import numpy as np
from typing import List, Tuple

from util import calculate_makespan

# Define the Simulated Annealing algorithm for JSSP
def simulated_annealing(
		jobs: List[List[Tuple[int, int]]], 
		num_jobs: int, 
		num_machines: int, 
		initial_temp: int, 
		final_temp: float, 
		alpha: float
	) -> Tuple[List[List[Tuple[int, int]]], int, List[Tuple[int, int]]]:
	# Helper function to generate a neighbor solution
	def generate_neighbor(solution: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
		neighbor = np.array(solution, copy = True)
		job_id = random.randint(0, num_jobs - 1)

		if len(neighbor[job_id]) > 1:
			i, j = random.sample(range(len(neighbor[job_id])), 2)
			neighbor[job_id][i], neighbor[job_id][j] = neighbor[job_id][j], neighbor[job_id][i]

		return neighbor

	# Initialize the current solution with the given jobs
	current_solution = jobs
	current_makespan = calculate_makespan(current_solution, num_machines, num_jobs)
	
	best_solution = current_solution
	best_makespan = current_makespan

	history = []
	
	temp = initial_temp
	
	iteration = 0
	while temp > final_temp:
		new_solution = generate_neighbor(current_solution)
		new_makespan = calculate_makespan(new_solution, num_machines, num_jobs)

		if new_makespan < current_makespan:
			current_solution = new_solution
			current_makespan = new_makespan
			
			if new_makespan < best_makespan:
				best_solution = new_solution
				best_makespan = new_makespan
		else:
			acceptance_probability = math.exp((current_makespan - new_makespan) / temp)
			if random.random() < acceptance_probability:
				current_solution = new_solution
				current_makespan = new_makespan

		temp *= alpha
		iteration += 1

		history.append((iteration, best_makespan))

	return best_solution, best_makespan, history