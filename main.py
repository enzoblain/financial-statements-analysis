from finance_data_processing.filings import get_filtered_filings
from finance_data_processing.statements import extract_statement_file_names

def main():
    try:
        accession_numbers = get_filtered_filings(is_10k=False, return_accession_numbers=True)
        if not accession_numbers.empty:
            accession_number = accession_numbers.iloc[0].replace("-", "")
            print(extract_statement_file_names(accession_number))
        else:
            print("No accession numbers found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
