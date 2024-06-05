import numpy as np

def calculate_makespan(schedule, num_machines, num_jobs):
	machine_times = np.zeros(num_machines, dtype=int)
	job_times = np.zeros(num_jobs, dtype=int)

	for job_id, operations in enumerate(schedule):
		for machine, duration in operations:
			start_time = max(machine_times[machine], job_times[job_id])
			finish_time = start_time + duration
			machine_times[machine] = finish_time
			job_times[job_id] = finish_time

	return machine_times.max()