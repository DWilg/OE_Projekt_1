# Klasa obsługująca algorytm

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


def genetic_algorithm(pop_size, epochs, selection_method):
    history = []
    best_solution = None
    np.random.seed(42)

    for epoch in range(epochs):
        best_value = np.random.rand()
        history.append(best_value)
        best_solution = best_value 
        time.sleep(0.1)

    return history, best_solution