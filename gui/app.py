import tkinter as tk
from algorithms.genetic_algorithm import GeneticAlgorithm
from optimization.benchmark_functions import test_function

def run_algorithm():
    ga = GeneticAlgorithm(population_size=50, num_generations=100, mutation_rate=0.05, crossover_rate=0.8)
    ga.evolve(test_function)
    print("Optymalizacja zakończona")

root = tk.Tk()
root.title("Algorytm Genetyczny")

btn = tk.Button(root, text="Start", command=run_algorithm)
btn.pack()

root.mainloop()