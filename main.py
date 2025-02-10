import argparse
import requests
import json
import sys

# Function to retrieve data from the given URL
def fetch_crime_data(url, page_start, page_size):
    try:
        response = requests.get(url, params={"$offset": page_start, "$limit": page_size})
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as err:
        # Handle any network or request-related errors
        print(f"Error occurred while fetching data: {err}")
        return []  # Return an empty list on failure

# Function to convert the fetched data into a formatted string
def format_crime_data(data):
    formatted_lines = []
    thorn_symbol = "\u00fe"  # Unicode for Thorn character (þ)

    for entry in data:
        crime_description = entry.get("narrative", "")
        reported_on = entry.get("report_date", "")
        offense_on = entry.get("offense_date", "")
        latitude = entry.get("latitude", "")
        longitude = entry.get("longitude", "")

        # Append the formatted record
        formatted_lines.append(f"{crime_description}{thorn_symbol}{reported_on}{thorn_symbol}{offense_on}{thorn_symbol}{latitude}{thorn_symbol}{longitude}")

    return "\n".join(formatted_lines)

def main():
    # Setting up command-line arguments
    parser = argparse.ArgumentParser(description="Fetch and format crime data from a given URL.")
    parser.add_argument("--url", type=str, required=True, help="URL to fetch crime data from.")
    parser.add_argument("--offset", type=int, required=True, help="Offset for pagination (start).")
    parser.add_argument("--limit", type=int, required=True, help="Limit for number of records to retrieve.")
    
    args = parser.parse_args()

    # Fetch the crime data
    crime_data = fetch_crime_data(args.url, args.offset, args.limit)
    
    # Format the fetched data into the required output format
    formatted_output = format_crime_data(crime_data)
    
    # Print the formatted data
    print(formatted_output)

if __name__ == "__main__":
    main()
