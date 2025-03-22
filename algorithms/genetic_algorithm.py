import numpy as np
from algorithms.selection import tournament_selection
from algorithms.crossover import one_point_crossover
from algorithms.mutation import bit_flip_mutation
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
    def __init__(self, population_size, num_generations, mutation_rate, crossover_rate, num_variables, inversion_rate=0.1):
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_variables = num_variables
        self.inversion_rate = inversion_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        return np.random.randint(2, size=(self.population_size, self.num_variables))

    def evaluate_population(self, function):
        return np.array([function(ind) for ind in self.population])

    def evolve(self, function):
        for generation in range(self.num_generations):
            fitness_scores = self.evaluate_population(function)
            parents = tournament_selection(self.population, fitness_scores, 3)
            offspring = one_point_crossover(parents, self.crossover_rate)
            mutated_offspring = bit_flip_mutation(offspring, self.mutation_rate)
            self.population = inversion(mutated_offspring, self.inversion_rate)
