# Implementacja inwersji
import numpy as np

def inversion(population):
    for i in range(len(population)):
        if np.random.rand() < 0.1: 
            start, end = sorted(np.random.randint(0, len(population[i]), size=2))
            population[i][start:end] = population[i][start:end][::-1]
    return population