import json
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Use a supported Gemini model
model_name = "models/gemini-2.5-flash"

# Your prompt template
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

# Function to call Gemini API and parse response
def extract_from_description(description):
    try:
        response = genai.GenerativeModel(model_name).generate_content(PROMPT + description.strip())
        content = response.text.strip()
        print("Gemini response:\n", content)

        # Extract JSON from text
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            return json.loads(content[start:end])
        raise ValueError("No valid JSON found in the response.")
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

# Load JSON, process, and enrich
def enrich_json_with_description_data(infile, outfile):
    with open(infile) as f:
        jobs = json.load(f)

    for job in jobs:
        if "job_description" in job:
            print(f"\nProcessing: {job.get('position', 'Unknown')}")
            job["from_description"] = extract_from_description(job["job_description"])
            time.sleep(1.5)  # to avoid rate limits

    with open(outfile, "w") as f:
        json.dump(jobs, f, indent=2)

# Run script
if __name__ == "__main__":
    enrich_json_with_description_data("jobs_deduplicated.json", "jobs_enriched_gemini.json")
