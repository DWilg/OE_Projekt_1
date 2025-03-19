# Implementacja mutacji
import numpy as np

def bit_flip_mutation(offspring, mutation_rate):
    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            if np.random.rand() < mutation_rate:
                offspring[i][j] = 1 - offspring[i][j]
    return offspring