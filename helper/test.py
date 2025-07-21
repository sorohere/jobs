import json

def clean_json_file(input_path, output_path):
    with open(input_path, "r") as infile:
        data = json.load(infile)

    for entry in data:
        if "from_description" in entry:
            desc = entry["from_description"]
            # Prioritize values from from_description if they are not "Not specified"
            for field in ["salary", "location", "job_type", "remote_status"]:
                desc_value = desc.get(field, "Not specified")
                entry_value = entry.get(field, "Not specified")
                if desc_value != "Not specified":
                    entry[field] = desc_value
                elif entry_value == "Not specified":
                    entry[field] = "Not specified"
            # Pull other fields directly
            for key in ["experience_level", "required_skills", "education", "technologies", "job_responsibilities"]:
                if key in desc:
                    entry[key] = desc[key]
            # Remove the nested object
            del entry["from_description"]

    with open(output_path, "w") as outfile:
        json.dump(data, outfile, indent=2)

# Example usage
clean_json_file("jobs.json", "jobs_output.json")
