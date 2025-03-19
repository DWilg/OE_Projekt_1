# import argparse
# from gui.app import run_gui
from algorithms.genetic_algorithm import GeneticAlgorithm
# from optimization.benchmark_functions import test_function
import numpy as np
def fitness_function(chromosome):
    return sum(chromosome)


if __name__ == "__main__":
    ga = GeneticAlgorithm(population_size=20, num_generations=50, mutation_rate=0.05, crossover_rate=0.8)
    ga.evolve(fitness_function)

    best_chromosome = max(ga.population, key=fitness_function)
    print("Najlepszy osobnik:", best_chromosome)
    print("Maksymalna wartość funkcji celu:", fitness_function(best_chromosome))

