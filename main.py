from functions.data_fetcher import save_data
from functions.data_selection import get_data
from functions.calcul import calculate_wr
from utils.config import CONFIGURATION, DATA
from functions.data_visualization import display
from functions.data_fetcher import save_data
from functions.calcul import find_range

def main() -> None:
    save_data()
    print(f'{CONFIGURATION["SYMBOL"]} : {calculate_wr(CONFIGURATION["SYMBOL"])}%')
    display()
    save_data(CONFIGURATION['SYMBOL'])
    find_range(DATA['BALANCE_SHEET'], 'inventory', 'Apple', 'AAPL')

if __name__ == "__main__":
    main()