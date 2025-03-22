import tkinter as tk
from tkinter import ttk
from algorithms.genetic_algorithm import GeneticAlgorithm
from optimization.benchmark_functions import test_function

def run_algorithm(population_size, num_generations, mutation_rate, crossover_rate):
    ga = GeneticAlgorithm(
        population_size=population_size,
        num_generations=num_generations,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        num_variables=10 
    )
    ga.evolve(test_function)
    print("Optymalizacja zakończona")

def run_gui():
    root = tk.Tk()
    root.title("Algorytm Genetyczny")

    # Opis GUI
    tk.Label(root, text="Rozmiar populacji:").pack()
    population_size_entry = tk.Entry(root)
    population_size_entry.insert(tk.END, "50")
    population_size_entry.pack()

    tk.Label(root, text="Liczba generacji:").pack()
    num_generations_entry = tk.Entry(root)
    num_generations_entry.insert(tk.END, "100")
    num_generations_entry.pack()

    tk.Label(root, text="Prawdopodobieństwo mutacji:").pack()
    mutation_rate_entry = tk.Entry(root)
    mutation_rate_entry.insert(tk.END, "0.05")
    mutation_rate_entry.pack()

    tk.Label(root, text="Prawdopodobieństwo krzyżowania:").pack()
    crossover_rate_entry = tk.Entry(root)
    crossover_rate_entry.insert(tk.END, "0.8")
    crossover_rate_entry.pack()

    def start_algorithm():
        population_size = int(population_size_entry.get())
        num_generations = int(num_generations_entry.get())
        mutation_rate = float(mutation_rate_entry.get())
        crossover_rate = float(crossover_rate_entry.get())
        run_algorithm(population_size, num_generations, mutation_rate, crossover_rate)

    btn = tk.Button(root, text="Start", command=start_algorithm)
    btn.pack()

    root.mainloop()

if __name__ == "__main__":
    run_gui()