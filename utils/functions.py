import os

from dotenv import load_dotenv

def get_fred_api_key():
    load_dotenv()

    FRED_API_KEY = os.getenv('FRED_API_KEY')

    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY not found. Please set it in the .env file.")

    return FRED_API_KEY