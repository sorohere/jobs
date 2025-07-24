import json
import csv
import sys
import os

def json_to_csv(json_file_path, csv_file_path=None):
    # If output CSV path is not given, use the same name with .csv extension
    
    if csv_file_path is None:
        csv_file_path = os.path.splitext(json_file_path)[0] + '.csv'

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            if not isinstance(data, list):
                raise ValueError("JSON must be a list of dictionaries.")

            # Get the fieldnames from the first record
            fieldnames = data[0].keys()

            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"CSV file created successfully: {csv_file_path}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_to_csv.py input_file.json [output_file.csv]")
    else:
        json_path = sys.argv[1]
        csv_path = sys.argv[2] if len(sys.argv) > 2 else None
        json_to_csv(json_path, csv_path)
