import sys
import numpy as np
import time
import sqlite3
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel,
    QSpinBox, QComboBox, QWidget, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from genetic_alforithm import genetic_algorithm



class GeneticApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Algorytm Genetyczny - GUI")
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()

        self.pop_label = QLabel("Populacja:")
        self.pop_size = QSpinBox()
        self.pop_size.setRange(10, 500)
        self.pop_size.setValue(100)

        self.epoch_label = QLabel("Epoki:")
        self.epochs = QSpinBox()
        self.epochs.setRange(10, 1000)
        self.epochs.setValue(100)

        self.selection_label = QLabel("Selekcja:")
        self.selection_method = QComboBox()
        self.selection_method.addItems(["Ruletka", "Turniejowa", "Elitarna"])

        self.start_button = QPushButton("Uruchom Algorytm")
        self.start_button.clicked.connect(self.run_algorithm)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        control_layout.addWidget(self.pop_label)
        control_layout.addWidget(self.pop_size)
        control_layout.addWidget(self.epoch_label)
        control_layout.addWidget(self.epochs)
        control_layout.addWidget(self.selection_label)
        control_layout.addWidget(self.selection_method)
        control_layout.addWidget(self.start_button)

        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def run_algorithm(self):
        pop_size = self.pop_size.value()
        epochs = self.epochs.value()
        selection = self.selection_method.currentText()

        start_time = time.time()
        history, best_solution = genetic_algorithm(pop_size, epochs, selection)
        exec_time = time.time() - start_time

        self.update_plot(history)

        print(f"Najlepsze rozwiązanie: {best_solution}")
        print(f"Czas wykonania: {exec_time:.2f} s")

    def update_plot(self, history):
        self.ax.clear()
        self.ax.plot(history, label="Wartość funkcji")
        self.ax.set_xlabel("Iteracja")
        self.ax.set_ylabel("Wartość")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneticApp()
    window.show()
    sys.exit(app.exec())
