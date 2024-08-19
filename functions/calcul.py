import pandas as pd
import matplotlib.pyplot as plt
from functions.polynomial_fit import determine_best_polynomial_degree, fit_polynomial_curve
from functions.data_selection import select_data
from utils.config import VALUES

def find_range(df, param, name, symbol):
    param_data = df.loc[param]
    param_data = pd.to_numeric(param_data, errors='coerce').dropna()

    if not pd.api.types.is_datetime64_any_dtype(param_data.index):
        param_data.index = pd.to_datetime(param_data.index)

    param_data = param_data[::-1]

    plt.figure(figsize=(12, 6))

    plt.plot(param_data.index, param_data.values, marker='o', linestyle='-', color='b', label='Original Data')

    best_degree = determine_best_polynomial_degree(param_data)
    fit_polynomial_curve(param_data, linestyle='--', degree=best_degree, color='red', label=f'Best Fit Polynomial (Degree {best_degree})')

    plt.title(f'{name} Over Time ({symbol})')
    plt.xlabel('Date')
    plt.ylabel(name)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def calculate_wr(symbol):
    current_data = {}
    average_data = {}

    for value in VALUES:
        name = value['Title']
        param = value['Data-title']
        folder = value['Data-file']
        current_flag = ['Current data']
        current_data[name] = select_data(symbol, param, folder, current_flag, True)
        average_data[name] = select_data(symbol, param, folder, current_flag, False)

    current_data['Average Total Assets'] = (
        (current_data['Current Assets'] + current_data['Old Current Assets']) / 2
    )
    average_data['Average Total Assets'] = (
        (average_data['Current Assets'] + average_data['Old Current Assets']) / 2
    )

    # Return on Equity : Measures how effectively management is using a company’s assets to create profits
    current_roe = current_data['Net Income'] / current_data['Shareholders Equity']
    average_roe = average_data['Net Income'] / average_data['Shareholders Equity']

    # Gross Margin Ratio: Shows how much of every dollar of sales is gross profit
    current_gmr = current_data['Gross Profit'] / current_data['Total Revenue']
    average_gmr = average_data['Gross Profit'] / average_data['Total Revenue']

    # Current Ratio: Measures the ability of a company to pay short-term obligations with short-term assets
    current_cr = current_data['Current Assets'] / current_data['Current Liabilities']
    average_cr = average_data['Current Assets'] / average_data['Current Liabilities']

    # Asset Turnover Ratio: Indicates how efficiently a company uses its assets to generate sales
    current_atr = current_data['Total Revenue'] / current_data['Average Total Assets']
    average_atr = average_data['Total Revenue'] / average_data['Average Total Assets']

    # Debt-to-Equity Ratio: Measures a company's financial leverage and compares total liabilities to shareholders' equity
    current_dter = current_data['Total Liabilities'] / current_data['Shareholders Equity']
    average_dter = average_data['Total Liabilities'] / average_data['Shareholders Equity']

    roer = current_roe / average_roe
    gmrr = current_gmr / average_gmr
    crr = current_cr / average_cr
    atrr = current_atr / average_atr
    dterr = current_dter / average_dter

    performance_ratio = (
        roer * 0.3 + 
        gmrr * 0.25 + 
        crr * 0.15 + 
        atrr * 0.15 + 
        dterr * 0.15
    ) * 100

    return round(performance_ratio)