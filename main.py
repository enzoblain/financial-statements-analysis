import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from fredapi import Fred
import os
import time
import re

from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv('FRED_API_KEY')

if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found. Please set it in the .env file.")

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    webpage_content = response.text
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

soup = BeautifulSoup(webpage_content, "lxml")

table = soup.find("table",{"id":"constituents"})
symbolList = []

for element in table.find_all("tr")[1:]:
    cell = element.find("td")
    symbolList.append(cell.text.strip())

def get_user_agent():
    response = requests.get("http://httpbin.org/user-agent")
    user_agent = response.json()['user-agent']
    return user_agent

def window(dataArray,window):
    movedArray = [0]*len(dataArray)

    for i,element in enumerate(dataArray):
        moveTo = i + window
        if moveTo < len(dataArray):
            movedArray[moveTo] = element
        else: 
            break
    
    return movedArray

def NANtreatment(arrayOne,arrayTwo):

    try:
        zeroOccurencies = (arrayTwo==0).sum()
    
    except:
        zeroOccurencies = sum([1 for x in arrayTwo if x==0])

    return arrayOne[zeroOccurencies:],arrayTwo[zeroOccurencies:]

def SNPessentials():

    SNP = yf.download("^GSPC",start="2024-01-01")["Close"]
    SNPmoved = window(SNP,1)

    SNPone,SNPtwo = NANtreatment(SNP,SNPmoved)
    SNPreturn = SNPone/SNPtwo - 1

    return SNPreturn


def calculateBeta(table):

    betatable = {}
    SNPreturn = SNPessentials()
    SNPreturnmean = np.mean(SNPreturn)

    for ticker in table.columns:
        
        sharemean = np.mean(table[ticker])

        cov = (sum((table[ticker]-sharemean)*(SNPreturn-SNPreturnmean)))/(len(table[ticker])-1)

        varRm = sum((SNPreturn-SNPreturnmean)**(2))/(len(SNPreturn)-1)

        betatable[ticker.split("_")[1]] = cov/varRm
    
    return betatable

def Rf():
    
    fred = Fred(api_key=FRED_API_KEY)

    # Fetch the latest 10-year Treasury yield
    treasury_yield = fred.get_series_latest_release('TB3MS')

    # Convert percentage to decimal
    risk_free_rate = (1+ treasury_yield / 100)**(12/3) - 1

    return risk_free_rate
    

def calculateCAPM(beta):

    CAPMdata = {}

    rf = Rf().iloc[-1]

    SNPreturn = SNPessentials()

    SNPmean = np.mean(SNPreturn)

    for ticker,beta in beta.items():

        CAPMdata[ticker] = float(rf + beta*(SNPmean-rf))
    
    return CAPMdata

def listAll(symbolList,batch_size=10):

    finalTable = pd.DataFrame()

    for i in range(0, len(symbolList), batch_size):
        batch_symbols = symbolList[i:i+batch_size]
        batch_data = yf.download(batch_symbols, start="2024-01-01")["Close"]

        for element in batch_symbols:
            TempTable = pd.DataFrame()
            TempTable[element] = batch_data[element]

            if element in TempTable.columns:
                TempTable["Temp"] = window(TempTable[element], 1)
                arrayOne, arrayTwo = NANtreatment(TempTable[element], TempTable["Temp"])

                finalTable = pd.concat([finalTable, arrayOne.to_frame(name=element), arrayTwo.to_frame(name="Temp")], axis=1)

                del TempTable
                del finalTable[element]
                del finalTable["Temp"]

                finalTable["Returns_" + element] = (arrayOne / arrayTwo) - 1

            else:
                print(f"{element} not found in TempTable.columns")

    return finalTable

def isFileInDirectory(file_name, directory_path):
    
    full_path = os.path.join(directory_path, file_name)
    
    return os.path.isfile(full_path)

def retrieveCIK(ticker,headers):

    ticker = ticker.upper()
    requestTickers = requests.get('https://www.sec.gov/files/company_tickers.json',headers=headers)

    requestTickersJSON = requestTickers.json()
    
    if requestTickers.status_code != 200:
        raise ValueError(f"Failed to retrieve data from SEC with status code {requestTickers.status_code}")

    for company in requestTickersJSON.values():
        if ticker == company["ticker"]:

            CIK = str(company["cik_str"]).zfill(10)

            return CIK

def getFilings(ticker,headers):

    try:
        CIK =  retrieveCIK(ticker,headers)
        print(CIK)
        
        if not CIK:
            raise ValueError(f"CIK for ticker {ticker} could not be retrieved.")
        
        urlFillings = f"https://data.sec.gov/submissions/CIK{CIK}.json"
        response = requests.get(urlFillings, headers=headers)
        response.raise_for_status()

        if response.status_code != 200:
            raise ValueError(f"Received unexpected status code {response.status_code}")
        
        if response.headers.get('Content-Type') != 'application/json':
            raise ValueError("Response content is not JSON")
        
        try:
            requestFilings = response.json()
        except ValueError:
            raise ValueError("Response content is not valid JSON")

        return pd.DataFrame(requestFilings["filings"]["recent"])

    except:
        raise ValueError(f"Unable to find {ticker} in SEC database")


def filterFilings(ticker,headers,ten_k = False,just_accession_numbers = False):

    fillings = getFilings(ticker,headers)

    if ten_k:
        df = fillings[fillings["form"]=="10-K"]
    else:
        df = fillings[fillings["form"]=="10-Q"]
    
    if just_accession_numbers:

        df = df.set_index("reportDate")
        accessionDf = df["accessionNumber"]

        return accessionDf

    else:
        
        return df

def getFacts(ticker,headers):

    CIK = retrieveCIK(ticker,headers)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"

    companyfacts = requests.get(url,headers = headers).json()

    return companyfacts

def _get_file_name(report):
    html_file_name_tag = report.find("HtmlFileName")
    xml_file_name_tag = report.find("XmlFileName")

    if html_file_name_tag:
        return html_file_name_tag.text
    elif xml_file_name_tag:
        return xml_file_name_tag.text
    else:
        return ""

def _is_statement_file(short_name_tag, long_name_tag, file_name):
    return (
        short_name_tag is not None
        and long_name_tag is not None
        and file_name  # Check if file_name is not an empty string
        and "Statement" in long_name_tag.text
    )


def factsTable(ticker,headers):

    facts = getFacts(ticker,headers)['facts']['us-gaap']

    factsTable = []

    for fact, values in facts.items():
        for item in values["units"]:
            for unitobject in values["units"][item]:

                row = unitobject.copy()
                row["fact"] = fact

                factsTable.append(row)
    
    factsDF = pd.DataFrame(factsTable)
    factsDF["end"] = pd.to_datetime(factsDF["end"])
    factsDF["start"] = pd.to_datetime(factsDF["start"])

    factsDF = factsDF.drop_duplicates(subset=["end","val","fact"])
    factsDF.set_index("end",inplace = True)

    return factsDF

def searchOccurencies(pattern,liste):
    
    indexListe = []
    index = 0
    for element in liste:
        match = re.findall(pattern,element)

        if match:
            indexListe.append(index)
        
        index += 1


    return [liste[i] for i in indexListe]

def get_statement_file_names_in_filing_summary(
    ticker, accession_number, headers
):
    try:
        session = requests.Session()

        session.headers.update(headers)

        cik = retrieveCIK(ticker,headers)
        base_link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}"
        filing_summary_link = f"{base_link}/FilingSummary.xml"
        print(filing_summary_link)

        filing_summary_response = session.get(filing_summary_link).content.decode("utf-8")

        filing_summary_soup = BeautifulSoup(filing_summary_response, "lxml-xml")
        statement_file_names_dict = {}

        for report in filing_summary_soup.find_all("Report"):
            file_name = _get_file_name(report)
            short_name, long_name = report.find("ShortName"), report.find("LongName")

            if _is_statement_file(short_name, long_name, file_name):
                statement_file_names_dict[short_name.text.lower()] = file_name

        return statement_file_names_dict

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

headers = {"User-Agent": "cxline.prod@gmail.com"}

accessions = filterFilings("AAPL",headers,ten_k = False,just_accession_numbers = True)

accession_number = accessions.iloc[0].replace("-","")
print(accession_number)

print(get_statement_file_names_in_filing_summary("AAPL",accession_number,headers))