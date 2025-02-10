import argparse
import requests
import json
import sys

def fetch_crime_data(url, page_start, page_size):
    """Fetch crime data from the given URL using the provided offset and limit."""
    try:
        response = requests.get(url, params={"$offset": page_start, "$limit": page_size})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred while fetching data: {err}", file=sys.stderr)
        return []

def read_local_crime_data(file_path):
    """Read crime data from a local JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return []

def filter_by_date(data, date_prefix):
    """Return only those records whose report_date starts with date_prefix."""
    if not date_prefix:
        return data
    return [entry for entry in data if entry.get("report_date", "").startswith(date_prefix)]

def filter_by_narrative(data, excluded_narratives):
    """Exclude records whose narrative field matches any in the excluded_narratives list."""
    if not excluded_narratives:
        return data
    return [entry for entry in data if entry.get("narrative", "") not in excluded_narratives]

def sort_by_report_date(data, descending=True):
    """Sort the records by report_date (ISO string) in descending order (most recent first)."""
    return sorted(data, key=lambda entry: entry.get("report_date", ""), reverse=descending)

def format_crime_data(data):
    """Format each record with the thorn character (þ) separating fields."""
    thorn_symbol = "\u00fe"  # Unicode for þ
    formatted_lines = []
    for entry in data:
        line = (
            f"{entry.get('narrative','')}{thorn_symbol}"
            f"{entry.get('report_date','')}{thorn_symbol}"
            f"{entry.get('offense_date','')}{thorn_symbol}"
            f"{entry.get('latitude','')}{thorn_symbol}"
            f"{entry.get('longitude','')}"
        )
        formatted_lines.append(line)
    return "\n".join(formatted_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and format crime data from a given URL or local file."
    )
    parser.add_argument("--url", type=str, help="URL to fetch crime data from.")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination (start).")
  
    parser.add_argument("--limit", type=int, default=10, help="Number of records to output after filtering.")
    parser.add_argument("--file", type=str, help="Path to a local JSON file with crime data.")
    parser.add_argument("--date", type=str, default="", 
                        help="Filter records by report_date starting with this value (e.g., '2025-01-20').")
   
    parser.add_argument("--exclude", type=str, nargs="*", default=[],
                        help="List of narrative values to exclude (e.g. 'Drug Violation').")
    
    args = parser.parse_args()
    

    fetch_size = args.limit * 2 + args.offset

    if args.file:
        crime_data = read_local_crime_data(args.file)
    elif args.url:
        crime_data = fetch_crime_data(args.url, args.offset, fetch_size)
    else:
        print("Error: Either --url or --file must be provided.", file=sys.stderr)
        sys.exit(1)
    

    crime_data = filter_by_date(crime_data, args.date)

    crime_data = filter_by_narrative(crime_data, args.exclude)
 
    crime_data = sort_by_report_date(crime_data, descending=True)
    
    crime_data = crime_data[args.offset:args.offset + args.limit]
    
    output = format_crime_data(crime_data)
    print(output)

if __name__ == "__main__":
    main()
