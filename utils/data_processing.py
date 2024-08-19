from finance_data_processing.cik import fetch_cik_for_ticker

import numpy as np
import pandas as pd

def apply_moving_window(data_array, window_size):
    if not isinstance(data_array, np.ndarray):
        raise ValueError("Input data_array must be a numpy array.")
    
    if not isinstance(window_size, int) or window_size < 0:
        raise ValueError("Window size must be a non-negative integer.")
    
    moved_array = np.zeros_like(data_array)
    
    for i in range(len(data_array)):
        move_to = i + window_size
        if move_to < len(data_array):
            moved_array[move_to] = data_array[i]
    
    return moved_array


def handle_zero_occurrences(array_one, array_two):
    if not isinstance(array_one, np.ndarray) or not isinstance(array_two, np.ndarray):
        raise TypeError("Both inputs must be numpy arrays.")
    
    if len(array_one) != len(array_two):
        raise ValueError("The lengths of the two arrays must be the same.")
    
    try:
        zero_occurrences = np.sum(array_two == 0)
    except Exception as e:
        raise RuntimeError(f"Error occurred while counting zero occurrences: {e}")

    return array_one[zero_occurrences:], array_two[zero_occurrences:]

def facts_table() -> pd.DataFrame:
    try:
        facts = fetch_cik_for_ticker()['facts']['us-gaap']
    except KeyError as e:
        raise ValueError(f"Unexpected data structure in API response: {e}")

    facts_table = []

    for fact, values in facts.items():
        for item, units in values["units"].items():
            for unit in units:
                row = unit.copy()
                row["fact"] = fact
                facts_table.append(row)

    facts_df = pd.DataFrame(facts_table)

    facts_df["end"] = pd.to_datetime(facts_df["end"], errors='coerce')
    facts_df["start"] = pd.to_datetime(facts_df["start"], errors='coerce')

    facts_df = facts_df.drop_duplicates(subset=["end", "val", "fact"])

    facts_df.set_index("end", inplace=True)

    return facts_df
