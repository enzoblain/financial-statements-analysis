import requests
from bs4 import BeautifulSoup

def fetch_sp500_symbols():
    """
    Retrieves the list of S&P 500 companies and their stock symbols from the Wikipedia page.

    This function performs the following steps:
    1. Sends an HTTP GET request to the Wikipedia page listing S&P 500 companies.
    2. Checks if the request was successful.
    3. Parses the webpage content to extract the stock symbols from the table with id 'constituents'.
    4. Returns a list of stock symbols.

    Returns:
    - List[str]: A list of stock symbols of S&P 500 companies.

    Raises:
    - RuntimeError: If the HTTP request fails or the response is not as expected.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            webpage_content = response.text
        else:
            raise RuntimeError(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        
        soup = BeautifulSoup(webpage_content, "lxml")
        
        table = soup.find("table", {"id": "constituents"})
        if not table:
            raise RuntimeError("Failed to find the table with S&P 500 companies.")
        
        symbol_list = []
        for row in table.find_all("tr")[1:]:
            cell = row.find("td")
            if cell:
                symbol_list.append(cell.text.strip())
        
        return symbol_list

    except requests.RequestException as e:
        raise RuntimeError(f"HTTP request failed: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the webpage: {e}")