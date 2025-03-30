import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from algorithms.genetic_algorithm import GeneticAlgorithm
from optimization.benchmark_functions import \
    Hypersphere, Rastrigin, \
    Hyperellipsoid
import numpy as np
from utils import save_to_database
def run_algorithm(population_size, num_generations, mutation_rate, crossover_rate, inversion_rate, selection_method, crossover_method, mutation_method, test_function_name, num_variables):
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
        num_variables=num_variables,
        inversion_rate=inversion_rate,
        selection_method=selection_method,
        crossover_method=crossover_method,
        mutation_method=mutation_method
    )
    
    ga.evolve(test_function)  
    messagebox.showinfo("Info", "Optymalizacja zakończona")
    return ga

def plot_results(ga):
    generations = list(range(1, ga.num_generations + 1))
    best_values = ga.best_values  
    
    all_fitness_values = ga.all_fitness_values 

    mean_values = [np.mean(fitness) for fitness in all_fitness_values]
    std_deviation = [np.std(fitness) for fitness in all_fitness_values]

    plt.figure(figsize=(8, 5))

    plt.subplot(2, 1, 1)
    plt.plot(generations, best_values, label="Najlepsza wartość funkcji celu", color='blue')
    plt.xlabel("Generacja")
    plt.ylabel("Wartość funkcji")
    plt.title("Wartości funkcji celu w czasie")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(generations, std_deviation, label="Odchylenie standardowe", color='red')
    plt.xlabel("Generacja")
    plt.ylabel("Odchylenie standardowe")
    plt.title("Odchylenie standardowe wartości funkcji celu")
    plt.legend()

    plt.tight_layout()
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

    tk.Label(root, text="Liczba zmiennych:").pack()
    num_variables_entry = tk.Entry(root)
    num_variables_entry.insert(tk.END, "10") 
    num_variables_entry.pack()

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
    crossover_method = ttk.Combobox(root, values=["Jednopunktowe", "Dwupunktowe", "Jednorodne", "Ziarniste"])
    crossover_method.set("Jednopunktowe")
    crossover_method.pack()
    
    tk.Label(root, text="Metoda mutacji:").pack()
    mutation_method = ttk.Combobox(root, values=["Bit Flip", "Brzegowa", "Dwupunktowa"])
    mutation_method.set("Bit Flip")
    mutation_method.pack()
    
    def start_algorithm():
        try:
            population_size = int(population_size_entry.get())
            if population_size <= 0:
                raise ValueError("Rozmiar populacji musi być liczbą całkowitą większą od 0.")

            num_generations = int(num_generations_entry.get())
            if num_generations <= 0:
                raise ValueError("Liczba generacji musi być liczbą całkowitą większą od 0.")

            num_variables = int(num_variables_entry.get())
            if num_variables <= 0:
                raise ValueError("Liczba zmiennych musi być liczbą całkowitą większą od 0.")

            mutation_rate = float(mutation_rate_entry.get())
            if not (0 <= mutation_rate <= 1):
                raise ValueError("Prawdopodobieństwo mutacji musi być liczbą z zakresu [0, 1].")

            crossover_rate = float(crossover_rate_entry.get())
            if not (0 <= crossover_rate <= 1):
                raise ValueError("Prawdopodobieństwo krzyżowania musi być liczbą z zakresu [0, 1].")

            inversion_rate = float(inversion_rate_entry.get())
            if not (0 <= inversion_rate <= 1):
                raise ValueError("Prawdopodobieństwo inwersji musi być liczbą z zakresu [0, 1].")
            selected_selection_method = selection_method.get()
            selected_crossover_method = crossover_method.get()
            selected_mutation_method = mutation_method.get()
            selected_test_function = test_function.get()
            global ga
            ga = run_algorithm(population_size, num_generations, mutation_rate, crossover_rate, inversion_rate, selected_selection_method, selected_crossover_method, selected_mutation_method, selected_test_function, num_variables)
            plot_results(ga)
            save_to_database.save_results_to_db(ga)
    

            
        except ValueError as e:
            messagebox.showerror("Błąd danych wejściowych", str(e))
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")
            
    btn = tk.Button(root, text="Start", command=start_algorithm)           
    btn.pack()
    
    plot_btn = tk.Button(root, text="Pokaż wykres", command=lambda: plot_results(ga))
    plot_btn.pack()

    root.mainloop()
if __name__ == "__main__":
    run_gui()