import pandas as pd
import matplotlib.pyplot as plt
from functions.polynomial_fit import determine_best_polynomial_degree, fit_polynomial_curve
from functions.data_selection import get_data
from utils.config import CURVS
import tkinter as tk
from tkinter import ttk
from utils.config import CONFIGURATION, CURVS, VALUES
from functions.data_visualization import plot_index_evolution

def plot_index_evolution(symbol, name, param, folder):
    df = get_data(symbol, folder)
    transposed_df = df.T

    if param not in transposed_df.index:
        print(f"Error: '{param}' not found in DataFrame.")
        return

    param_data = transposed_df.loc[param]
    param_data = pd.to_numeric(param_data, errors='coerce').dropna()

    if not pd.api.types.is_datetime64_any_dtype(param_data.index):
        param_data.index = pd.to_datetime(param_data.index)

    param_data = param_data[::-1]

    plt.figure(figsize=(12, 6))

    plt.plot(param_data.index, param_data.values, marker='o', linestyle='-', color='b', label='Original Data')

    # if curvParams:
        # CURVS = curvParams

    for curv in CURVS:
        if curv['Show curv']:
            if curv['Average number'] == None:
                best_degree = determine_best_polynomial_degree(param_data)
                fit_polynomial_curve(param_data, linestyle=curv['Linestyle'], degree=best_degree, color=curv['Color'], label=f'{curv["Name"]} (Degree {best_degree})')
            else:
                ma = param_data.rolling(window=curv['Average number'], min_periods=1).mean()
                plt.plot(ma.index[curv['Average number'] - 1:], ma.values[curv['Average number'] - 1:], linestyle=curv['Linestyle'], color=curv['Color'], label=f'{curv["Average number"]}{curv["Name"]})')
        

    plt.title(f'{name} Over Time ({symbol})')
    plt.xlabel('Date')
    plt.ylabel(name)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def on_select(typed, value, title_to_id=None):
    if typed == 'SYMBOL':
        CONFIGURATION['SYMBOL'] = value
    elif typed == "GRAPH":
        selected_id = title_to_id[value]
        CONFIGURATION['GRAPH'] = VALUES[selected_id]

def display():
    root = tk.Tk()
    root.title("Data Visualisation")

    symbol_options = CONFIGURATION['SYMBOLS']
    symbol_choice = ttk.Combobox(root, values=symbol_options, state='readonly')
    symbol_choice.pack(pady=10)
    symbol_choice.set(CONFIGURATION['SYMBOL'])
    symbol_choice.bind("<<ComboboxSelected>>", lambda event: on_select('SYMBOL', symbol_choice.get()))

    title_to_id = {entry['Title']: entry['id'] for entry in VALUES}

    graph_choice = ttk.Combobox(root, values=list(title_to_id.keys()), state='readonly')
    graph_choice.pack(pady=10)
    graph_choice.set(CONFIGURATION['GRAPH']['Title'])
    graph_choice.bind("<<ComboboxSelected>>", lambda event: on_select('GRAPH', graph_choice.get(), title_to_id))

    for index, curve in enumerate(CURVS):
        frame = tk.Frame(root)
        frame.pack(pady=5)

        label_text = f"{str(curve['Average number']) + ' ' if curve['Average number'] is not None else ''}{curve['Name']}"
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=10)

        var = tk.BooleanVar(value=curve['Show curv'])
        button = tk.Checkbutton(frame, text="Show Curve", variable=var, command=lambda i=index, v=var: toggle_curve_state(i, v))
        button.pack(side=tk.RIGHT)

    button = tk.Button(root, text="Show Graph", command=lambda: plot_index_evolution(CONFIGURATION['SYMBOL'], CONFIGURATION['GRAPH']['Title'], CONFIGURATION['GRAPH']['Data-title'], CONFIGURATION['GRAPH']['Data-file']))
    button.pack(pady=20)

    root.mainloop()

def toggle_curve_state(index, var):
    CURVS[index]['Show curv'] = var.get()

if __name__ == "__main__":
    display()