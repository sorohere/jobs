import json

# Load the original JSON file
with open("jobs_deduplicated.json", "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Number of chunks
num_parts = 8
chunk_size = len(data) // num_parts
remainder = len(data) % num_parts

start = 0
for i in range(num_parts):
    # Adjust chunk size to distribute remainder across the first few files
    end = start + chunk_size + (1 if i < remainder else 0)
    part = data[start:end]
    
    # Save to new JSON file
    output_filename = f"part_{i+1}.json"
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(part, outfile, ensure_ascii=False, indent=2)
    
    print(f"Saved {output_filename} with {len(part)} records")
    start = end
