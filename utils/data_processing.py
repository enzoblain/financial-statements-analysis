from finance_data_processing.cik import fetch_cik_for_ticker

import numpy as np
import pandas as pd

def apply_moving_window(data_array, window_size):
    """
    Applies a moving window to a given array, shifting elements by the specified window size.

    This function creates a new array where each element from the original array is moved forward by 
    the specified number of positions (window size). The positions at the start of the new array will 
    be filled with zeros if the window size causes the elements to move out of bounds.

    Parameters:
        data_array (np.ndarray): The input array to which the moving window will be applied.
        window_size (int): The number of positions to shift each element in the array.

    Returns:
        np.ndarray: An array with the elements moved forward by the window size. Elements that cannot
                    be moved forward due to the window size will be zero.

    Raises:
        ValueError: If the input is not a numpy array or if the window size is not a positive integer.
    """
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
    """
    Removes elements from the beginning of two arrays based on the number of zero occurrences in the second array.

    This function calculates the number of zero values in `array_two` and uses that count to slice both `array_one`
    and `array_two`, effectively removing the same number of elements from the start of both arrays.

    Parameters:
        array_one (np.ndarray): The first array from which elements will be removed.
        array_two (np.ndarray): The second array used to determine how many elements to remove from `array_one`.

    Returns:
        tuple: A tuple containing two numpy arrays:
            - The first array with the specified number of elements removed from the start.
            - The second array with the same number of elements removed from the start.

    Raises:
        TypeError: If `array_one` and `array_two` are not numpy arrays.
        ValueError: If the lengths of `array_one` and `array_two` are not the same.
    """
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
    """
    Retrieves and processes financial facts for a given ticker and returns a DataFrame with the relevant data.

    This function fetches financial facts from an API, processes the data, and formats it into a DataFrame.
    The DataFrame includes columns for the fact name, values, start and end dates, and is indexed by the end date.

    Returns:
        pd.DataFrame: A DataFrame containing financial facts with columns for fact, value, start date, and end date.
    
    Raises:
        ValueError: If the data structure from the API response is not as expected.
    """
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
