# Financial Statement Analyzer

This project provides a Python tool for analyzing financial statements of corporations. It leverages the `fredapi` to retrieve economic data, and various other libraries to process and analyze the data.

## Features

- Retrieve economic data using the FRED API.
- Analyze and visualize financial statements.
- Utilize pandas, numpy, and other libraries for data processing.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python 3.x installed on your system. You will also need to install the required Python packages listed in `requirements.txt`.

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/enzoblain/financial-statements-analysis
cd financial-statement-analyzer
```
2. **Set Up a Virtual Environment (Optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. **Install Dependencies**

```bash
pip install -r requirements.txt
```
4. **Set Up FRED API Key**

To use the FRED API, you need an API key. Follow these steps to get your API key:

- Sign up for a free API key at FRED API website.

- Save your API key in a .env file in the root directory of the project with the following format:

```makefile
FRED_API_KEY=your_api_key_here
```

### Usage

1. **Run the Main Script**

Execute the main script to start analyzing financial statements:

```bash
python main.py
```
The script will fetch data from FRED, process it, and output the analysis.

2. **Customize Analysis**

You can modify the main.py file to tailor the analysis according to your needs. Refer to the script's comments for guidance on how to adjust the analysis.

### Project Structure
- main.py : The main script to run the financial statement analysis.
requirements.txt: Lists the Python dependencies required for the project.
- .env : Store your FRED API key here.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Make sure to follow the coding style and include tests where applicable.

## Contact
For any questions or issues, please open an issue on the GitHub repository or contact blenzodu57@gmail.com.