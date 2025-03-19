# Implementacja krzyżowania


import numpy as np

def one_point_crossover(parents, crossover_rate):
    offspring = []
    for i in range(0, len(parents), 2):
        if np.random.rand() < crossover_rate:
            point = np.random.randint(1, len(parents[0]))
            child1 = np.concatenate((parents[i][:point], parents[i+1][point:]))
            child2 = np.concatenate((parents[i+1][:point], parents[i][point:]))
            offspring.extend([child1, child2])
        else:
            offspring.extend([parents[i], parents[i+1]])
    return np.array(offspring)