import json
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Prompt for extraction
PROMPT = """
You are an information extraction AI. You will receive a full job description. You must extract the following fields **only if they are explicitly mentioned**, and return the result as a valid JSON object. If any field is not present, write `"Not specified"`.

Example Input 1:
---
Microsoft is hiring a Software Engineer with 3+ years experience in C++ and Python. Candidates should have a Bachelor's degree in Computer Science or related field. The role is on-site in Bengaluru and is full-time.
---
Expected Output 1:
{
  "experience_level": "3+ years",
  "required_skills": ["C++", "Python"],
  "education": "Bachelor's degree in Computer Science or related field",
  "job_type": "Full-time",
  "location": "Bengaluru",
  "salary": "Not specified",
  "remote_status": "On-site",
  "technologies": ["C++", "Python"],
  "job_responsibilities": "Not specified"
}

Example Input 2:
---
Join our startup to work on cutting-edge NLP research. We're hiring interns to assist with research in PyTorch and Hugging Face Transformers. Remote work is allowed.
---
Expected Output 2:
{
  "experience_level": "Intern",
  "required_skills": ["PyTorch", "Hugging Face Transformers"],
  "education": "Not specified",
  "job_type": "Internship",
  "location": "Not specified",
  "salary": "Not specified",
  "remote_status": "Remote",
  "technologies": ["PyTorch", "Hugging Face Transformers"],
  "job_responsibilities": "Assist with NLP research using PyTorch and Transformers"
}

Now extract the information from this job description. Follow the format exactly. Do not assume or guess. Do not return any explanation or commentary. Only valid JSON.

Job Description:
---
"""

# Function to extract fields from a single job description
def extract_from_description(description):
    try:
        full_prompt = PROMPT + description.strip() + "\n---"
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[{"role": "user", "content": full_prompt}],
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            }
        )
        content = response.choices[0].message.content.strip()

        print("Model response:\n", content)  # Debug print

        # Attempt to extract JSON from response
        first_brace = content.find('{')
        last_brace = content.rfind('}') + 1

        if first_brace != -1 and last_brace != -1:
            json_str = content[first_brace:last_brace]
            return json.loads(json_str)

        raise ValueError("No valid JSON found in model output.")

    except Exception as e:
        print("Error:", e)
        return {
            "experience_level": "Not specified",
            "required_skills": "Not specified",
            "education": "Not specified",
            "job_type": "Not specified",
            "location": "Not specified",
            "salary": "Not specified",
            "remote_status": "Not specified",
            "technologies": "Not specified",
            "job_responsibilities": "Not specified"
        }

# Function to enrich each job in a JSON file with extracted info
def enrich_json_with_description_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        jobs = json.load(f)

    for job in jobs:
        if "job_description" in job:
            print(f"\nProcessing: {job.get('position', 'Unknown')}")
            job["from_description"] = extract_from_description(job["job_description"])
            time.sleep(1.5)  # Pause to respect API limits

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

# Usage example
if __name__ == "__main__":
    enrich_json_with_description_data("temp.json", "jobs_enriched.json")
