from utils.functions import get_fred_api_key

FRED_API_KEY = get_fred_api_key()
HEADERS = {"User-Agent": "cxline.prod@gmail.com"}
TICKER = "AAPL"