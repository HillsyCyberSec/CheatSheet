import pandas as pd
import requests
from io import StringIO
from tabulate import tabulate

# URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/HillsyCyberSec/CheatSheet/main/CheatSheet.csv'

def load_data(url):
    """Load CSV data from a URL into a DataFrame."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        csv_data = response.text
        data = StringIO(csv_data)
        df = pd.read_csv(data, delimiter=',')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def query_data(dataframe, queries):
    """Query the DataFrame for multiple search terms in all columns."""
    if dataframe is not None:
        # Create a mask for each query term and combine them with AND logic
        mask = pd.Series([True] * len(dataframe))
        for query in queries:
            mask &= dataframe.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
        results = dataframe[mask]
        return results
    else:
        print("No data to query.")
        return pd.DataFrame()

def display_results(results):
    """Display results in a formatted table."""
    if not results.empty:
        # Convert the DataFrame to a list of lists (table format)
        table = results.values.tolist()
        headers = results.columns.tolist()

        # Set max column width
        max_width = 30
        wrapped_table = [[('\n'.join([line[i:i+max_width] for i in range(0, len(line), max_width)])) if isinstance(line, str) else line for line in row] for row in table]

        # Print the table using tabulate with a grid format
        print("\nMatching results:")
        print(tabulate(wrapped_table, headers, tablefmt="grid"))
    else:
        print("No matching results found.")

def main():
    # Load the data
    df = load_data(csv_url)
    
    # Prompt the user for multiple search terms
    queries = input("Enter your search terms (separate by commas): ").split(',')
    queries = [query.strip() for query in queries]  # Strip any extra whitespace
    
    # Query the data
    results = query_data(df, queries)
    
    # Display the results
    display_results(results)

if __name__ == "__main__":
    main()
