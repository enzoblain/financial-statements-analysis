import pandas as pd
from utils.config import CONFIGURATION

def select_data(symbol, param, folder, current, average):
    data = get_data(symbol, folder)
    transposed_data = data.T

    if param not in transposed_data.index:
        print(f"Error: '{param}' not found in data")
        return pd.DataFrame() 

    selected_data = transposed_data.loc[param]

    if average:
        numeric_values = selected_data.apply(pd.to_numeric, errors='coerce')
        average = numeric_values.mean()
        return average

    place = 0 if current else 1
    return selected_data.iloc[place]

def get_data(symbol, folder):
    path = f'{CONFIGURATION["DATA_DIR"]}/{symbol}/{folder}'

    if not path:
        print("Error: No file path provided")
        return pd.DataFrame() 

    try:
        df = pd.read_csv(path)
        df.set_index(df.columns[0], inplace=True)
        return df
    except Exception as e:
        print(f"Error loading data from {path}: {e}")
        return pd.DataFrame()
