CONFIGURATION = {
    'API_KEY' : 'VTJ1MO76Y9KU8W7M',
    'START_DATE' : '2001-01-01',
    'DATA_DIR': 'data',
    'SYMBOLS' : ['AAPL', 'MSFT', 'GOOGL'],
    'SYMBOL' : 'AAPL',
    'UPDATE' : False,
    'GRAPH' : {
        'Title' : 'Net Income',
        'Data-title' : 'netIncome',
        'Data-file' : 'Quarterly_income_statement.csv',
    },
    'TRANSPOSED' : True
}

PARTS = {
    'BALANCE_SHEET': 'Quarterly_balance_sheet.csv',
    'INCOME_STATEMENT': 'Quarterly_income_statement.csv',
    'CASH_FLOW': 'Quarterly_cash_flow.csv'
}

VALUES = [
    {
        'id' : 0,
        'Title' : 'Net Income', #
        'Data-title' : 'netIncome', #
        'Data-file' : 'Quarterly_income_statement.csv', #
        'Current data' : True,
        'Show data' : False
    },
    {
        'id' : 1,
        'Title' : 'Shareholders Equity', 
        'Data-title' : 'totalShareholderEquity', 
        'Data-file' : 'Quarterly_balance_sheet.csv',
        'Current data' : True,
        'Show data' : True
    },
    {
        'id' : 2,
        'Title' : 'Gross Profit', 
        'Data-title' : 'grossProfit', 
        'Data-file' : 'Quarterly_income_statement.csv',
        'Current data' : True,
        'Show data' : False
    },
    {
        'id' : 3,
        'Title' : 'Total Revenue',
        'Data-title' : 'totalRevenue', 
        'Data-file' : 'Quarterly_income_statement.csv',
        'Current data' : True,
        'Show data' : False
    },
    {
        'id' : 4,
        'Title' : 'Current Assets', 
        'Data-title' : 'totalCurrentAssets', 
        'Data-file' : 'Quarterly_balance_sheet.csv',
        'Current data' : True,
        'Show data' : False
    },
    {
        'id' : 5,
        'Title' : 'Old Current Assets', 
        'Data-title' : 'totalCurrentAssets', 
        'Data-file' : 'Quarterly_balance_sheet.csv',
        'Current data' : False,
        'Show data' : False
    },
    {
        'id' : 6,
        'Title' : 'Current Liabilities',
        'Data-title' : 'totalCurrentLiabilities', 
        'Data-file' : 'Quarterly_balance_sheet.csv',
        'Current data' : True,
        'Show data' : False
    },
    {
        'id' : 7,
        'Title' : 'Total Liabilities', 
        'Data-title' : 'totalLiabilities', 
        'Data-file' : 'Quarterly_balance_sheet.csv',
        'Current data' : True,
        'Show data' : False
    }
]

CURVS = [
    {
        'Name' : '-Point Moving Average ',
        'Color' : 'orange',
        'Average number' : 20,
        'Linestyle' : '--',
        'Show curv' : False
    },
    {
        'Name' : '-Point Moving Average ',
        'Color' : 'green',
        'Average number' : 10,
        'Linestyle' : '--',
        'Show curv' : False
    },
    {
        'Name' : '-Point Moving Average ',
        'Color' : 'red',
        'Average number' : 5,
        'Linestyle' : '--',
        'Show curv' : False
    },
    {
        'Name' : '-Point Moving Average ',
        'Color' : 'purple',
        'Average number' : 2,
        'Linestyle' : '--',
        'Show curv' : False
    },
    {
        'Name' : 'Best Fit Polynomial ',
        'Color' : 'red',
        'Average number' : None,
        'Linestyle' : '-',
        'Show curv' : True
    }
]

DATA = {}