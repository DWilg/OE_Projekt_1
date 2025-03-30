import os
import time
import numpy as np
import matplotlib.pyplot as plt
from algorithms.genetic_algorithm import GeneticAlgorithm
from optimization.benchmark_functions import Rastrigin

# Testy przeprowadzone 10 razy dla każdej  poniżeszj konfiguracji i liczby zmiennych 10
# Wykresy przedstawiające średnie wartości funkcji celu oraz czas wykonania
# dla każdej konfiguracji
def compare_configurations():
    if not os.path.exists('results'):
        os.makedirs('results')
    configurations = [
        {
            "name": "Konfiguracja bazowa",
            "params": {
                "selection": "Turniejowa",
                "crossover": "Jednopunktowe",
                "mutation": "Bit Flip",
                "mutation_rate": 0.1,
                "crossover_rate": 0.9,
                "population_size": 50,
                "num_generations": 100
            }
        },
        {
            "name": "Wysoka mutacja",
            "params": {
                "selection": "Turniejowa",
                "crossover": "Jednopunktowe",
                "mutation": "Bit Flip",
                "mutation_rate": 0.2,
                "crossover_rate": 0.9,
                "population_size": 50,
                "num_generations": 100
            }
        },
        {
            "name": "Krzyżowanie dwupunktowe",
            "params": {
                "selection": "Turniejowa",
                "crossover": "Dwupunktowe",
                "mutation": "Bit Flip",
                "mutation_rate": 0.1,
                "crossover_rate": 0.9,
                "population_size": 50,
                "num_generations": 100
            }
        },
        {
            "name": "Koło ruletki + niska mutacja",
            "params": {
                "selection": "Koło ruletki",
                "crossover": "Jednopunktowe",
                "mutation": "Bit Flip",
                "mutation_rate": 0.05,
                "crossover_rate": 0.9,
                "population_size": 50,
                "num_generations": 100
            }
        }
    ]
    
    results = []
    best_runs = []  
    
    for config in configurations:
        config_best_values = []
        config_times = []
        all_runs_data = [] 
        
        print(f"Testowanie konfiguracji: {config['name']}...")
        
        for run in range(10):
            start_time = time.time()
            ga = GeneticAlgorithm(
                population_size=config["params"]["population_size"],
                num_generations=config["params"]["num_generations"],
                mutation_rate=config["params"]["mutation_rate"],
                crossover_rate=config["params"]["crossover_rate"],
                num_variables=10,
                selection_method=config["params"]["selection"],
                crossover_method=config["params"]["crossover"],
                mutation_method=config["params"]["mutation"]
            )
            ga.evolve(Rastrigin()._evaluate)
            final_best = min(ga.best_values)
            config_best_values.append(final_best)
            elapsed_time = time.time() - start_time
            config_times.append(elapsed_time)
            
            all_runs_data.append({
                "best_values": ga.best_values.copy(),
                "std_deviation": [np.std(fitness) for fitness in ga.all_fitness_values],
                "time": elapsed_time
            })
        
        mean_value = np.mean(config_best_values)
        best_value = min(config_best_values)
        worst_value = max(config_best_values)
        mean_time = np.mean(config_times)
        std_time = np.std(config_times)
        
        best_run_idx = np.argmin(config_best_values)
        best_runs.append({
            "config_name": config["name"],
            "best_values": all_runs_data[best_run_idx]["best_values"],
            "std_deviation": all_runs_data[best_run_idx]["std_deviation"],
            "time": all_runs_data[best_run_idx]["time"]
        })
        
        results.append({
            "config_name": config["name"],
            "mean_value": mean_value,
            "best_value": best_value,
            "worst_value": worst_value,
            "mean_time": mean_time,
            "std_time": std_time,
            "all_values": config_best_values
        })
        
    csv_path = os.path.join('results', "comparison_results.csv")
    with open(csv_path, "w", encoding='utf-8') as f:
        f.write("Konfiguracja,Średnia wartość,Najlepsza wartość,Najgorsza wartość,Średni czas [s],Odchylenie czasu [s]\n")
        for res in results:
            f.write(f"{res['config_name']},{res['mean_value']:.4f},{res['best_value']:.4f},{res['worst_value']:.4f},{res['mean_time']:.4f},{res['std_time']:.4f}\n")
    
    plt.figure(figsize=(10, 7))
    
    plt.subplot(2, 2, 1)
    bars = plt.bar([res["config_name"] for res in results], [res["mean_value"] for res in results])
    plt.title("Średnie wartości funkcji celu (10 powtórzeń)", fontsize=10)
    plt.ylabel("Wartość funkcji", fontsize=8)
    plt.xticks(rotation=15, fontsize=8)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom', fontsize=9)
    
    plt.subplot(2, 2, 2)
    bars = plt.bar([res["config_name"] for res in results], [res["mean_time"] for res in results],
            yerr=[res["std_time"] for res in results], capsize=5)
    plt.title("Średni czas wykonania (10 powtórzeń)", fontsize=10)
    plt.ylabel("Czas [s]", fontsize=8)
    plt.xticks(rotation=15, fontsize=8)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}s',
                 ha='center', va='bottom', fontsize=9)
    
    plt.subplot(2, 2, 3)
    for run in best_runs:
        plt.plot(run["best_values"], label=f"{run['config_name']} (czas: {run['time']:.2f}s)")
    plt.title("Zbieżność algorytmu (najlepsze uruchomienie)", fontsize=10)
    plt.xlabel("Generacja", fontsize=8)
    plt.ylabel("Wartość funkcji", fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=8)
    
    plt.subplot(2, 2, 4)
    for run in best_runs:
        plt.plot(run["std_deviation"], label=run["config_name"])
    plt.title("Odchylenie standardowe populacji (najlepsze uruchomienie)", fontsize=10)
    plt.xlabel("Generacja", fontsize=8)
    plt.ylabel("Odchylenie standardowe", fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=9)
    
    plt.tight_layout()
        
    plot_path = os.path.join('results', 'comparison_results.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()  
    
    plt.figure(figsize=(10, 6))
    for res in results:
        plt.scatter([res["config_name"]]*len(res["all_values"]), res["all_values"], 
                   alpha=0.5, label=res["config_name"])
    plt.title("Rozkład wyników dla wszystkich uruchomień", fontsize=10)
    plt.ylabel("Wartość funkcji", fontsize=8)
    plt.xticks(rotation=15, fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.close()
    
    return results

results = compare_configurations()