import pandas as pd
import requests
from io import StringIO
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tabulate import tabulate

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

def load_csv_from_url(url):
    """
    Load the CSV file directly from the GitHub URL into a DataFrame.
    """
    print(f"Loading CSV from {url}...")
    try:
        response = requests.get(url)  # SSL verification suppressed by warning filter
        response.raise_for_status()  # Raise an error for bad responses
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, on_bad_lines='warn')  # Updated parameter
        df.columns = df.columns.str.strip()  # Strip whitespace from column names
        print("CSV loaded successfully.")
        print("Column names:", df.columns.tolist())  # Print column names for verification
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def query_tool(dataframe, tool_name):
    """
    Query the DataFrame for rows containing the specified tool name.
    """
    if dataframe is not None:
        # Convert tool_name to lower case
        tool_name_lower = tool_name.lower()
        
        # Verify that 'Tools' column exists
        if 'Tools' in dataframe.columns:
            # Convert the 'Tools' column to lower case and perform the search
            results = dataframe[dataframe['Tools'].str.lower().str.contains(tool_name_lower, na=False)]
            return results
        else:
            print("'Tools' column not found in DataFrame.")
            return pd.DataFrame()
    else:
        print("No data available to query.")
        return pd.DataFrame()

def main():
    # GitHub URL to the raw CSV file
    csv_url = 'https://raw.githubusercontent.com/HillsyCyberSec/CheatSheet/main/CheatSheet.csv'
    
    # Load the CSV file into a DataFrame
    df = load_csv_from_url(csv_url)
    
    if df is not None:
        # Ask the user for the tool name to query
        tool_name = input("Enter the name of the tool to search for: ")
        
        # Query the DataFrame
        results = query_tool(df, tool_name)
        
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

