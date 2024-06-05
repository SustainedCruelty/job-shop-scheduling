import numpy as np

from util import calculate_makespan

def greedy_scheduling(jobs, num_jobs, num_machines):
    
    # Prepare data structures
    machine_availability = np.zeros(num_machines, dtype=int)
    job_completion = np.zeros(num_jobs, dtype=int)
    schedule = [[] for _ in range(num_jobs)]
    
    # Flatten all operations and sort them by duration (SPT)
    operations = []
    for job_id, job_operations in enumerate(jobs):
        for machine_id, duration in job_operations:
            operations.append((duration, job_id, machine_id))
    operations.sort()
    
    # Process each operation, respecting machine and job constraints
    for duration, job_id, machine_id in operations:
        # Update the schedule for this job
        schedule[job_id].append((machine_id, duration))
    
    return schedule, calculate_makespan(schedule, num_jobs, num_machines)