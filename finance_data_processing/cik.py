from utils.config import HEADERS, TICKER

import requests

def fetch_cik_for_ticker():
    try:
        ticker = TICKER.upper()
        url = 'https://www.sec.gov/files/company_tickers.json'
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        tickers_data = response.json()
        cik = next((str(data.get("cik_str", "")).zfill(10) for data in tickers_data.values() if ticker == data.get("ticker")), None)
        if cik:
            return cik
        else:
            raise ValueError(f"CIK not found for ticker {TICKER}")
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data processing error: {e}")