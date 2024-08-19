from finance_data_processing.cik import fetch_cik_for_ticker
from utils.config import HEADERS, TICKER

import requests
import pandas as pd

def fetch_recent_filings():
    try:
        cik = fetch_cik_for_ticker()
        if not cik:
            raise ValueError(f"CIK for ticker {TICKER} could not be retrieved.")
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        filings_data = response.json()
        return pd.DataFrame(filings_data.get("filings", {}).get("recent", []))
    except Exception as e:
        raise RuntimeError(f"Error fetching filings: {e}")

def get_filtered_filings(is_10k=False, return_accession_numbers=False):
    filings_df = fetch_recent_filings()
    form_type = "10-K" if is_10k else "10-Q"
    filtered_df = filings_df[filings_df["form"] == form_type]

    if return_accession_numbers:
        return filtered_df.set_index("reportDate")["accessionNumber"]
    else:
        return filtered_df
