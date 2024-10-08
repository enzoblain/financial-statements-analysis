from utils.config import FRED_API_KEY
from snp500.snp500_analysis import calculate_snp_returns

from fredapi import Fred

import pandas as pd
import yfinance as yf

def calculate_risk_free_rate():
    if not FRED_API_KEY:
        raise RuntimeError("FRED_API_KEY environment variable is not set.")
    
    try:
        fred = Fred(api_key=FRED_API_KEY)

        treasury_yield = fred.get_series_latest_release('TB3MS')

        risk_free_rate = (1 + treasury_yield / 100) ** (12 / 3) - 1

        return risk_free_rate

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process data: {str(e)}")

import numpy as np

def calculate_capm(beta_values):
    try:
        risk_free_rate = calculate_risk_free_rate()
        if risk_free_rate is None:
            raise RuntimeError("Unable to retrieve the risk-free rate.")

        sp500_returns = calculate_snp_returns()
        if sp500_returns.empty:
            raise RuntimeError("S&P 500 returns data is empty.")
        
        sp500_mean_return = np.mean(sp500_returns)

        capm_results = {}
        for ticker, beta in beta_values.items():
            capm_return = risk_free_rate + beta * (sp500_mean_return - risk_free_rate)
            capm_results[ticker] = float(capm_return)
        
        return capm_results

    except Exception as e:
        raise RuntimeError(f"Error calculating CAPM: {str(e)}")

from utils.data_processing import apply_moving_window, handle_zero_occurrences 

def list_all(symbols, batch_size=10):
    final_table = pd.DataFrame()

    for i in range(0, len(symbols), batch_size):
        batch_symbols = symbols[i:i+batch_size]
        
        batch_data = yf.download(batch_symbols, start="2024-01-01")["Close"]
        
        for symbol in batch_symbols:
            if symbol in batch_data.columns:
                temp_table = pd.DataFrame()
                temp_table[symbol] = batch_data[symbol]

                temp_table["Temp"] = apply_moving_window(temp_table[symbol], 1)
                array_one, array_two = handle_zero_occurrences(temp_table[symbol], temp_table["Temp"])

                returns = (array_one / array_two) - 1
                final_table = pd.concat([final_table, returns.rename("Returns_" + symbol)], axis=1)
            else:
                print(f"Warning: {symbol} not found in batch data")

    return final_table