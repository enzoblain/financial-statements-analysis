from utils.data_processing import apply_moving_window, handle_zero_occurrences

import numpy as np
import pandas as pd
import yfinance as yf

def calculate_snp_returns(start_date="2024-01-01"):
    try:
        snp_data = yf.download("^GSPC", start=start_date)
        if 'Close' not in snp_data.columns:
            raise ValueError("Closing price data is missing from the retrieved data.")

        snp_close = snp_data["Close"]

        snp_moved = apply_moving_window(snp_close, 1)

        snp_cleaned, snp_moved_cleaned = handle_zero_occurrences(snp_close.to_numpy(), snp_moved.to_numpy())

        snp_returns = (snp_cleaned / snp_moved_cleaned) - 1

        return snp_returns

    except Exception as e:
        raise RuntimeError(f"An error occurred while calculating S&P 500 returns: {str(e)}")

def calculate_beta(returns_table):
    if not isinstance(returns_table, pd.DataFrame) or returns_table.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame.")
    
    beta_values = {}
    
    sp500_returns = calculate_beta()
    sp500_mean_return = np.mean(sp500_returns)
    
    for ticker in returns_table.columns:
        stock_returns = returns_table[ticker]
        
        covariance = np.cov(stock_returns, sp500_returns, ddof=0)[0, 1]
        
        sp500_variance = np.var(sp500_returns, ddof=0)
        
        beta_values[ticker.split("_")[1]] = covariance / sp500_variance
    
    return beta_values, sp500_mean_return