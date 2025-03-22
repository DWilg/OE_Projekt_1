import numpy as np
from algorithms.selection import roulette_selection, tournament_selection
from algorithms.crossover import one_point_crossover, two_point_crossover, uniform_crossover
from algorithms.mutation import bit_flip_mutation, boundary_mutation
from algorithms.inversion import inversion


#Kanoniczna postać AG z książki Tomasza Gwiazdy Algorytmy genetyczne

# Algorytm

# 1. t =1
# 2. generuj populacje 
# 3. do while warunek_konca_jest_spelniony=False
# 4. Ocen populacje P(t)
# 5. z populacji P(t) wyselekcjonuj zbiór rodziców Q 
# 6. Sotsujac operacje genetyczne na Q utwórz potomków
# 7. Utwórz nowa populacje P(t+1)
# 8. t= t+1
# 9. loop


class GeneticAlgorithm:
    def __init__(self, population_size, num_generations, mutation_rate, crossover_rate, num_variables, inversion_rate=0.1, selection_method="Turniejowa", crossover_method="Jednopunktowe", mutation_method="Bit Flip"):
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_variables = num_variables
        self.inversion_rate = inversion_rate
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.population = self.initialize_population()
        self.best_values = [] 

    def fitness(self, individual):
        return sum(individual)
    
    def initialize_population(self):
        return np.random.randint(2, size=(self.population_size, self.num_variables))

    def evaluate_population(self):
        return np.array([self.fitness(ind) for ind in self.population])

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
        else:
            raise ValueError("Unknown crossover method: " + self.crossover_method)

    def mutate(self, offspring):
        if self.mutation_method == "Bit Flip":
            return bit_flip_mutation(offspring, self.mutation_rate)
        elif self.mutation_method == "Brzegowa":
            return boundary_mutation(offspring, self.mutation_rate)
        else:
            raise ValueError("Unknown mutation method: " + self.mutation_method)

    def evolve(self, function):
        for generation in range(self.num_generations):
            fitness_scores = self.evaluate_population()
            self.best_values.append(np.max(fitness_scores))  # Store the best value of each generation (max)
            parents = self.select_parents(fitness_scores)
            offspring = self.crossover(parents)
            mutated_offspring = self.mutate(offspring)
            self.population = inversion(mutated_offspring, self.inversion_rate)