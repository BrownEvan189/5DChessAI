import torch
from torch import nn
import numpy as np
import pygad
from pygad import torchga

# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

# Define model
model = nn.Sequential(
            nn.Linear(3, 8),
            nn.ReLU(),
            nn.Linear(8, 5)
        ).to(device)

torch_ga = torchga.TorchGA(model=model, num_solutions=10)

# Data inputs
data_inputs = torch.tensor([[1.0, 2.0, 3.0]])#, [3.0, 1.0, 7.0], [2.0, 4.0, 3.0], [7.0, 5.0, 0.0], [3.0, 5.0, 2.0]])

# Data outputs
data_outputs = torch.tensor([[0.4, 0.1, 0.3, 0.15, 0.05]])#, [0.2, 0.35, 0.25, 0.13, 0.07], 
#[0.6, 0.19, 0.01, 0.12, 0.08], [0.17, 0.18, 0.21, 0.24, 0.2], [0.5, 0.25, 0.1, 0.05, 0.1]])

loss_function = torch.nn.KLDivLoss( reduction='batchmean')

def fitness_func(ga_instance, solution, sol_idx):
    global data_inputs, data_outputs, torch_ga, model, loss_function

    predictions = torchga.predict(model=model,
                                        solution=solution,
                                        data=data_inputs)

    solution_fitness = 1.0 / (loss_function(predictions, data_outputs).detach().numpy() + 0.00000001)

    return solution_fitness

def on_generation(ga_instance):
    print(f"Generation = {ga_instance.generations_completed}")

num_generations = 10000 # Number of generations.
num_parents_mating = 2 # Number of solutions to be selected as parents in the mating pool.
initial_population = torch_ga.population_weights # Initial population of network weights

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       initial_population=initial_population,
                       fitness_func=fitness_func,
                       on_generation=on_generation,
                       mutation_type="adaptive",
                       mutation_percent_genes=[30, 10])

ga_instance.run()

ga_instance.plot_fitness(title="PyGAD & PyTorch - Iteration vs. Fitness", linewidth=4)

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(f"Fitness value of the best solution = {solution_fitness}")
print(f"Index of the best solution : {solution_idx}")

predictions = pygad.torchga.predict(model=model,
                                    solution=solution,
                                    data=data_inputs)
print("Predictions : \n", predictions.detach().numpy())

# torch.save(model.state_dict(), "model.pth")
# print("Saved PyTorch Model State to model.pth")

# model = NeuralNetwork().to(device)
# model.load_state_dict(torch.load("model.pth"))
