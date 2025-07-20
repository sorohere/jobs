import json
import time
import os
from dotenv import load_dotenv
from tqdm import tqdm
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model_name = "models/gemini-2.5-flash"

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

def extract_from_description(description):
    try:
        response = genai.GenerativeModel(model_name).generate_content(PROMPT + description.strip())
        content = response.text.strip()

        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            return json.loads(content[start:end])
        raise ValueError("No valid JSON found in the response.")

    except Exception as e:
        error_message = str(e)
        if "quota" in error_message.lower() or "rate" in error_message.lower() or "expired" in error_message.lower():
            raise RuntimeError("Quota exceeded or API key issue: " + error_message)
        print("Non-critical error:", error_message)
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

def enrich_json_with_description_data(infile, outfile):
    with open(infile, "r") as f:
        jobs = json.load(f)

    enriched_jobs = []
    try:
        for job in tqdm(jobs, desc="Processing Jobs", unit="job"):
            print(f"\nProcessing: {job.get('position', 'Unknown')}")
            if "job_description" in job:
                job["from_description"] = extract_from_description(job["job_description"])
            else:
                job["from_description"] = {
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
            enriched_jobs.append(job)
            time.sleep(1.5)  # Prevent rate limiting

    except RuntimeError as quota_error:
        print("\n❌ API Limit Reached or Key Error. Saving progress so far...")
        with open(outfile, "w") as f:
            json.dump(enriched_jobs, f, indent=2)
        print("✅ Progress saved to:", outfile)
        return

    # Final save if all processed
    with open(outfile, "w") as f:
        json.dump(enriched_jobs, f, indent=2)
    print("\n✅ All jobs processed and saved to:", outfile)

if __name__ == "__main__":
    enrich_json_with_description_data("part_1.json", "part_1_enrich.json")
