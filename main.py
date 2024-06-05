from load_jssp_data import load_jssp_data
from simulated_annealing import simulated_annealing

file_path = '/opt/kobe-scheduling/data/jssp/abz/abz5.jss'

num_jobs, num_machines, jobs = load_jssp_data(file_path)

solution, makespan, history = simulated_annealing(
    jobs = jobs,
    num_jobs = num_jobs,
    num_machines = num_machines,
    initial_temp = 1000,
    final_temp = 0.1,
    alpha = 0.99
)

print(makespan)