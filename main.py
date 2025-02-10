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
        print(f"Error occurred while fetching data: {err}", file=sys.stderr)
        return []

# Function to read data from a local JSON file
def read_local_crime_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.", file=sys.stderr)
        return []

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
    parser = argparse.ArgumentParser(description="Fetch and format crime data from a given URL or local file.")
    parser.add_argument("--url", type=str, help="URL to fetch crime data from.")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination (start).")
    parser.add_argument("--limit", type=int, default=10, help="Limit for number of records to retrieve.")
    parser.add_argument("--file", type=str, help="Path to a local JSON file with crime data.")

    args = parser.parse_args()

    # Determine source of data (URL or local file)
    if args.file:
        crime_data = read_local_crime_data(args.file)
    elif args.url:
        crime_data = fetch_crime_data(args.url, args.offset, args.limit)
    else:
        print("Error: Either --url or --file must be provided.", file=sys.stderr)
        sys.exit(1)

    # Format the fetched data into the required output format
    formatted_output = format_crime_data(crime_data)

    # Print the formatted data
    print(formatted_output)

if __name__ == "__main__":
    main()
