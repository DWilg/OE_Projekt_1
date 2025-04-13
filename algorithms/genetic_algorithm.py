import os
import time

import numpy as np

from algorithms.crossover import \
    one_point_crossover, \
    two_point_crossover, \
    uniform_crossover, \
    granular_crossover
from algorithms.inversion import \
    inversion
from algorithms.mutation import \
    bit_flip_mutation, \
    boundary_mutation, \
    two_point_mutation
from algorithms.selection import \
    roulette_selection, \
    tournament_selection


class GeneticAlgorithm:
    def __init__(
            self,
            population_size,
            num_generations,
            mutation_rate,
            crossover_rate,
            num_variables,
            inversion_rate=0.1,
            selection_method="Turniejowa",
            crossover_method="Jednopunktowe",
            mutation_method="Bit Flip",
            elitism_rate=0.01,
            optimization_goal="min"  # "min" or "max"
    ):
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_variables = num_variables
        self.inversion_rate = inversion_rate
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.elitism_rate = elitism_rate
        self.optimization_goal = optimization_goal.lower()
        self.population = self.initialize_population()
        self.best_values = []
        self.all_fitness_values = []

    def initialize_population(self):
        return np.random.uniform(low=0.1, high=1.0, size=(self.population_size, self.num_variables))

    def evaluate_population(self, function):
        return np.array([function(ind) for ind in self.population])

    def select_parents(self, fitness_scores):
        if self.selection_method == "Turniejowa":
            return tournament_selection(self.population, fitness_scores, 3)
        elif self.selection_method == "Koło ruletki":
            return roulette_selection(self.population, fitness_scores)
        else:
            raise ValueError("Unknown selection method: " + self.selection_method)

    def crossover(self, parents):
        if self.crossover_method == "Jednopunktowe":
            return one_point_crossover(parents, self.crossover_rate)
        elif self.crossover_method == "Dwupunktowe":
            return two_point_crossover(parents, self.crossover_rate)
        elif self.crossover_method == "Jednorodne":
            return uniform_crossover(parents, self.crossover_rate)
        elif self.crossover_method == "Ziarniste":
            return granular_crossover(parents, self.crossover_rate)
        else:
            raise ValueError("Unknown crossover method: " + self.crossover_method)

    def mutate(self, offspring):
        if self.mutation_method == "Bit Flip":
            return bit_flip_mutation(offspring, self.mutation_rate)
        elif self.mutation_method == "Brzegowa":
            return boundary_mutation(offspring, self.mutation_rate)
        elif self.mutation_method == "Dwupunktowa":
            return two_point_mutation(offspring, self.mutation_rate)
        else:
            raise ValueError("Unknown mutation method: " + self.mutation_method)

    def evolve(self, function):
        if not os.path.exists('results'):
            os.makedirs('results')

        results = []
        start_time = time.time()

        for generation in range(self.num_generations):
            fitness_scores = self.evaluate_population(function)
            self.all_fitness_values.append(fitness_scores)

            if self.optimization_goal == "min":
                best_idx = np.argmin(fitness_scores)
                best_value = fitness_scores[best_idx]
                elite_indices = np.argsort(fitness_scores)[:max(1, int(self.elitism_rate * self.population_size))]
            elif self.optimization_goal == "max":
                best_idx = np.argmax(fitness_scores)
                best_value = fitness_scores[best_idx]
                elite_indices = np.argsort(fitness_scores)[::-1][:max(1, int(self.elitism_rate * self.population_size))]
            else:
                raise ValueError("Unknown optimization goal: use 'min' or 'max'")

            self.best_values.append(best_value)
            elites = self.population[elite_indices]

            print(f"Gen {generation + 1} | Best fitness: {best_value}")

            parents = self.select_parents(fitness_scores)
            offspring = self.crossover(parents)
            mutated_offspring = self.mutate(offspring)
            self.population = inversion(mutated_offspring, self.inversion_rate)

            self.population = np.vstack((elites, self.population))
            self.population = self.population[:self.population_size]

            results.append({
                'generation': generation + 1,
                'best_value': best_value,
                'time': time.time() - start_time
            })

        csv_path = os.path.join('results', 'algorithm_results.csv')
        with open(csv_path, 'w') as file:
            file.write("Generation,Best Value,Time\n")
            for result in results:
                file.write(f"{result['generation']},{result['best_value']},{result['time']}\n")

        end_time = time.time()
        print(f"Optymalizacja zakończona. Czas obliczeń: {end_time - start_time:.2f} sekundy.")

        return self