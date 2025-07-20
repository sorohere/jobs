import csv

def count_rows(csv_file):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        # Count the number of rows
        row_count = sum(1 for row in reader)
    return row_count

# Usage
csv_file = 'alljobs_with_description.csv'
print(f"Number of rows: {count_rows(csv_file)}")
