import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from algorithms.genetic_algorithm import GeneticAlgorithm
from optimization.benchmark_functions import \
    Hypersphere, Rastrigin, \
    Hyperellipsoid


def run_algorithm(population_size, num_generations, mutation_rate, crossover_rate, inversion_rate, selection_method, crossover_method, mutation_method, test_function_name):
    hypersphere = Hypersphere()
    rastrigin = Rastrigin()
    hyperellipsoid = Hyperellipsoid()
    def test_function(individual):
        if test_function_name == "Rastrigin":
            return rastrigin._evaluate(individual)
        elif test_function_name == "Hypersphere":
            return hypersphere._evaluate(individual)
        elif test_function_name == "Hyperellipsoid":
            return hyperellipsoid._evaluate(individual)
        print("Evaluating individual:", individual)


    ga = GeneticAlgorithm(
        population_size=population_size,
        num_generations=num_generations,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        num_variables=10,
        inversion_rate=inversion_rate,
        selection_method=selection_method,
        crossover_method=crossover_method,
        mutation_method=mutation_method
    )
    
    ga.evolve(test_function)  # tutaj do przekazania funkcja do przetestowaina dla nas 2
    messagebox.showinfo("Info", "Optymalizacja zakończona")
    return ga

def plot_results(ga):
    generations = list(range(1, ga.num_generations + 1))
    values = ga.best_values
    plt.figure(figsize=(6, 4))
    plt.plot(generations, values, label="Wartość funkcji celu")
    plt.xlabel("Generacja")
    plt.ylabel("Wartość")
    plt.title("Optymalizacja w czasie")
    plt.legend()
    plt.show()

def run_gui():
    root = tk.Tk()
    root.title("Algorytm Genetyczny")

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
    
    tk.Label(root, text="Prawdopodobieństwo inwersji:").pack()
    inversion_rate_entry = tk.Entry(root)
    inversion_rate_entry.insert(tk.END, "0.1")
    inversion_rate_entry.pack()

    tk.Label(root,
             text="Wybierz funkcję testową:").pack()
    test_function = tk.StringVar(
        value="Hypersphere")

    tk.Radiobutton(root,
                   text="Rastrigin",
                   variable=test_function,
                   value="Rastrigin").pack()
    tk.Radiobutton(root,
                   text="Hypersphere",
                   variable=test_function,
                   value="Hypersphere").pack()
    tk.Radiobutton(root,
                   text="Hyperellipsoid",
                   variable=test_function,
                   value="Hyperellipsoid").pack()

    tk.Label(root, text="Metoda selekcji:").pack()
    selection_method = ttk.Combobox(root, values=["Turniejowa", "Koło ruletki"])
    selection_method.set("Turniejowa")
    selection_method.pack()
    
    tk.Label(root, text="Metoda krzyżowania:").pack()
    crossover_method = ttk.Combobox(root, values=["Jednopunktowe", "Dwupunktowe", "Jednorodne"])
    crossover_method.set("Jednopunktowe")
    crossover_method.pack()
    
    tk.Label(root, text="Metoda mutacji:").pack()
    mutation_method = ttk.Combobox(root, values=["Bit Flip", "Brzegowa"])
    mutation_method.set("Bit Flip")
    mutation_method.pack()
    
    def start_algorithm():
        population_size = int(population_size_entry.get())
        num_generations = int(num_generations_entry.get())
        mutation_rate = float(mutation_rate_entry.get())
        crossover_rate = float(crossover_rate_entry.get())
        inversion_rate = float(inversion_rate_entry.get())
        selected_selection_method = selection_method.get()
        selected_crossover_method = crossover_method.get()
        selected_mutation_method = mutation_method.get()
        selected_test_function = test_function.get()
        global ga
        ga = run_algorithm(population_size, num_generations, mutation_rate, crossover_rate, inversion_rate, selected_selection_method, selected_crossover_method, selected_mutation_method, selected_test_function)
        plot_results(ga)
    
    btn = tk.Button(root, text="Start", command=start_algorithm)
    btn.pack()
    
    plot_btn = tk.Button(root, text="Pokaż wykres", command=lambda: plot_results(ga))
    plot_btn.pack()

    root.mainloop()

if __name__ == "__main__":
    run_gui()