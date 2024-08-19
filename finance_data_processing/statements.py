from finance_data_processing.cik import fetch_cik_for_ticker
from utils.utils import _get_file_name, _is_statement_file
from utils.config import HEADERS, TICKER

import requests

from bs4 import BeautifulSoup

def extract_statement_file_names(accession_number):
    try:
        cik = fetch_cik_for_ticker()
        if not cik:
            raise ValueError(f"CIK could not be retrieved for ticker {TICKER}")
        base_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"
        filing_summary_url = f"{base_url}/FilingSummary.xml"

        response = requests.get(filing_summary_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml-xml")
        file_names = {}
        for report in soup.find_all("Report"):
            file_name = _get_file_name(report)
            short_name = report.find("ShortName")
            long_name = report.find("LongName")

            if _is_statement_file(short_name, long_name, file_name):
                file_names[short_name.text.lower()] = file_name
        return file_names
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Error processing XML: {e}")