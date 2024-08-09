import subprocess
import sys
import pandas as pd
import requests
from io import StringIO
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib3.exceptions import NotOpenSSLWarning
from tabulate import tabulate

def install(package):
    """Install the package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_and_install_dependencies():
    """Check if required packages are installed and install them if not."""
    required_packages = ['pandas', 'requests', 'tabulate']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Package {package} not found. Installing...")
            install(package)

def load_csv_from_url(url):
    """Load the CSV file directly from the GitHub URL into a DataFrame."""
    print(f"Loading CSV from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, on_bad_lines='warn')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def query_all_columns(dataframe, search_terms):
    """Search all columns in the DataFrame for any of the specified search terms."""
    if dataframe is not None:
        search_terms_lower = [term.lower() for term in search_terms]
        
        def row_matches(row):
            row_str = row.astype(str).str.lower()
            return any(term in value for term in search_terms_lower for value in row_str)

        results = dataframe[dataframe.apply(row_matches, axis=1)]
        return results
    else:
        print("No data available to query.")
        return pd.DataFrame()

def main():
    """Main function to load data and perform the query."""
    # Check and install dependencies
    check_and_install_dependencies()

    # Import necessary libraries after ensuring they are installed
    import pandas as pd
    import requests
    from io import StringIO
    from tabulate import tabulate
    import warnings
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    from urllib3.exceptions import NotOpenSSLWarning

    # Suppress specific warnings
    warnings.simplefilter('ignore', InsecureRequestWarning)
    warnings.simplefilter('ignore', NotOpenSSLWarning)

    # GitHub URL to the raw CSV file
    csv_url = 'https://raw.githubusercontent.com/HillsyCyberSec/CheatSheet/main/CheatSheet.csv'

    # Load the CSV file into a DataFrame
    df = load_csv_from_url(csv_url)

    if df is not None:
        # Ask the user for multiple search terms
        search_terms = input("Enter the terms to search for (comma-separated): ").split(',')
        search_terms = [term.strip() for term in search_terms]

        # Query the DataFrame
        results = query_all_columns(df, search_terms)

        # Display the results in a table format
        if not results.empty:
            print("Matching results:")
            print(tabulate(results, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("No matches found.")
    else:
        print("Failed to load data.")

if __name__ == "__main__":
    main()

