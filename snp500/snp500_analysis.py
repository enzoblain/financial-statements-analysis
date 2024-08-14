from utils.data_processing import apply_moving_window, handle_zero_occurrences

import numpy as np
import pandas as pd
import yfinance as yf

def calculate_snp_returns(start_date="2024-01-01"):
    """
    Calculates the daily returns of the S&P 500 index starting from a specified date.

    This function downloads the historical closing prices of the S&P 500 index (^GSPC) from Yahoo Finance,
    computes the daily returns based on the moving window, and returns the calculated returns.

    Parameters:
        start_date (str): The start date for fetching the historical data in "YYYY-MM-DD" format. Default is "2024-01-01".

    Returns:
        np.Series: A Pandas Series containing the daily returns of the S&P 500 index.

    Raises:
        RuntimeError: If there is an error in retrieving or processing the data.
    """
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
    """
    Calculates the beta values of stocks relative to the S&P 500 index and returns the mean return of the S&P 500.

    Beta measures a stock's volatility relative to the overall market. This function computes beta values 
    using the covariance between stock returns and S&P 500 returns and the variance of S&P 500 returns. 
    Additionally, it calculates the mean return of the S&P 500 index.

    Parameters:
        returns_table (pd.DataFrame): DataFrame where each column represents the returns of a stock, 
                                      and each row represents a time period.

    Returns:
        tuple: A tuple containing:
            - dict: A dictionary where keys are stock tickers and values are the corresponding beta values.
            - float: The mean return of the S&P 500 index.
    
    Raises:
        ValueError: If the input table is not a pandas DataFrame or if it is empty.
    """
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