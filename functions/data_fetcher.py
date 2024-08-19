import os
import pandas as pd
import requests
from utils.config import CONFIGURATION, PARTS, DATA
from functions.data_selection import get_data

def get_alpha_vantage_data(function, symbol):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': function,
        'symbol': symbol,
        'apikey': CONFIGURATION['API_KEY']
    }
    response = requests.get(url, params=params)
    return response.json()

def filter_financial_data(data, statement_key, start_date):
    if statement_key not in data:
        print(f"Key '{statement_key}' not found in the data: {data}")
        return pd.DataFrame()

    filtered_data = [
        entry for entry in data.get(statement_key, [])
        if entry.get('fiscalDateEnding', '') > start_date
    ]
    return pd.DataFrame(filtered_data)

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

def save_data():
    for symbol in CONFIGURATION['SYMBOLS']:
        for function in PARTS.keys():
            symbol_dir = os.path.join(CONFIGURATION['DATA_DIR'], symbol)
            symbol_file = os.path.join(symbol_dir, PARTS[function])

            if not os.path.isdir(symbol_dir):
                os.makedirs(symbol_dir)

            if CONFIGURATION['UPDATE'] or not os.path.exists(symbol_file):
                data = get_alpha_vantage_data(function, symbol)
                df = filter_financial_data(data, 'quarterlyReports', CONFIGURATION['START_DATE'])
            else:
                df = pd.DataFrame()

            if not df.empty:
                save_to_csv(df, symbol_file)

def save_data(symbol):
    for file_name in PARTS.keys():
        data = get_data(symbol, PARTS[file_name])
        if CONFIGURATION['TRANSPOSED']:
            DATA[file_name] = data.T
        else:
            DATA[file_name] = data