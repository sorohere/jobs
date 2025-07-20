import json

def strip_specific_tail(text):
    tail = (
        "\n        \n\n        \n\n    \n    \n    \n\n    \n\n        \n            Show more\n"
        "          \n\n          \n    \n  \n\n        \n\n    \n    \n    \n\n    \n\n        \n"
        "            Show less"
    )
    if isinstance(text, str) and text.endswith(tail):
        return text[:-len(tail)].strip()
    return text

def clean_json_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for job in data:
        if 'job_description' in job:
            job['job_description'] = strip_specific_tail(job['job_description'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Set your file paths here
input_file = 'alljobs_with_description.json'
output_file = 'jobs_cleaned.json'

clean_json_file(input_file, output_file)
print(f"Cleaned descriptions saved to {output_file}")
