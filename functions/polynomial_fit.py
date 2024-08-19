import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def determine_best_polynomial_degree(data, max_degree = 5):
    x = np.arange(len(data))
    y = data.values

    x_train = x[:-1]
    y_train = y[:-1]

    best_degree = 1
    best_mse = float('inf')

    for degree in range(1, max_degree + 1):
        coefficients = np.polyfit(x_train, y_train, degree)
        polynomial = np.poly1d(coefficients)

        y_pred = polynomial(x_train)
        mse = mean_squared_error(y_train, y_pred)

        if mse < best_mse:
            best_mse = mse
            best_degree = degree

    return best_degree

def fit_polynomial_curve(data, linestyle, degree, color, label):
    x = np.arange(len(data))
    y = data.values

    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)

    x_fit = np.linspace(0, len(data) - 1, 100)
    y_fit = polynomial(x_fit)

    plt.plot(data.index[x_fit.astype(int)], y_fit, color=color, linestyle=linestyle, label=label)