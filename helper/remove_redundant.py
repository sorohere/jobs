import json

def remove_duplicates_by_description(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    seen_descriptions = set()
    unique_jobs = []

    for job in data:
        desc = job.get("job_description", "")
        if desc not in seen_descriptions:
            seen_descriptions.add(desc)
            unique_jobs.append(job)

    print(f"Original count: {len(data)}")
    print(f"Unique count  : {len(unique_jobs)}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_jobs, f, indent=2, ensure_ascii=False)

# Customize file paths as needed
input_file = 'jobs_cleaned.json'
output_file = 'jobs_deduplicated.json'

remove_duplicates_by_description(input_file, output_file)
print(f"Deduplicated data saved to {output_file}")
