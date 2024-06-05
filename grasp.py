import numpy as np
import random

def calculate_makespan(schedule, num_jobs, num_machines):
    machine_times = np.zeros(num_machines, dtype=int)
    job_times = np.zeros(num_jobs, dtype=int)

    for job_id, operations in enumerate(schedule):
        for machine, start_time, duration in operations:
            start_time = max(machine_times[machine], job_times[job_id])
            finish_time = start_time + duration
            machine_times[machine] = finish_time
            job_times[job_id] = finish_time

    return machine_times.max()

def greedy_randomized_construction(jobs, num_jobs, num_machines, alpha):
    machine_times = np.zeros(num_machines, dtype=int)
    job_times = np.zeros(num_jobs, dtype=int)
    schedule = [[] for _ in range(num_jobs)]

    operations = []
    for job_id, job_operations in enumerate(jobs):
        for machine_id, duration in job_operations:
            operations.append((duration, job_id, machine_id))
    
    while operations:
        min_duration = min(operations, key=lambda x: x[0])[0]
        max_duration = max(operations, key=lambda x: x[0])[0]
        threshold = min_duration + alpha * (max_duration - min_duration)
        
        restricted_list = [op for op in operations if op[0] <= threshold]
        
        chosen_operation = random.choice(restricted_list)
        operations.remove(chosen_operation)
        
        duration, job_id, machine_id = chosen_operation
        start_time = max(machine_times[machine_id], job_times[job_id])
        finish_time = start_time + duration
        
        schedule[job_id].append((machine_id, start_time, duration))
        machine_times[machine_id] = finish_time
        job_times[job_id] = finish_time

    return schedule

def local_search(schedule, num_jobs, num_machines):
    def swap_operations(schedule, job_id1, op_index1, job_id2, op_index2):
        new_schedule = [job[:] for job in schedule]
        new_schedule[job_id1][op_index1], new_schedule[job_id2][op_index2] = (
            new_schedule[job_id2][op_index2], new_schedule[job_id1][op_index1])
        return new_schedule

    best_schedule = schedule
    best_makespan = calculate_makespan(schedule, num_jobs, num_machines)

    improved = True
    while improved:
        improved = False
        for job_id1 in range(num_jobs):
            for op_index1 in range(len(schedule[job_id1])):
                for job_id2 in range(num_jobs):
                    for op_index2 in range(len(schedule[job_id2])):
                        if job_id1 != job_id2 or op_index1 != op_index2:
                            new_schedule = swap_operations(best_schedule, job_id1, op_index1, job_id2, op_index2)
                            new_makespan = calculate_makespan(new_schedule, num_jobs, num_machines)
                            if new_makespan < best_makespan:
                                best_schedule = new_schedule
                                best_makespan = new_makespan
                                improved = True

    return best_schedule

def grasp(jobs, num_jobs, num_machines, iterations, alpha):
    best_makespan = float('inf')
    best_solution = []

    for iteration in range(iterations):
        initial_schedule = greedy_randomized_construction(jobs, num_jobs, num_machines, alpha)
        improved_schedule = local_search(initial_schedule, num_jobs, num_machines)
        current_makespan = calculate_makespan(improved_schedule, num_jobs, num_machines)

        print(f"Iteration {iteration}: Makespan = {current_makespan}")
        if current_makespan < best_makespan:
            best_makespan = current_makespan
            best_solution = improved_schedule

    return best_solution, best_makespan