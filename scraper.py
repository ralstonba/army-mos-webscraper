import requests
import json
import re
import time

def get_job_sub_category(category):
    if category == "science-medicine":
        return "general-care"
    elif category == "mechanics-engineering":
        return "construction-engineering"
    elif category == "support-logistics":
        return "transportation-logistics"
    elif category == "signal-intelligence":
        return "cyber-intelligence"
    elif category == "aviation-aerial-defense":
        return "aviation"
    elif category == "ground-forces":
        return "combat"
    else:
        return "other"

def main():
    base_url = "https://www.goarmy.com"
    json_url = f"{base_url}/bin/aemservlet/cmtjobs.en.json"
    SCRIPT_TIMEOUT_SECONDS = 60  # 60 seconds for fail-fast

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    print(f"Fetching job list from: {json_url}")
    try:
        response = requests.get(json_url, headers=headers)
        response.raise_for_status()
        jobs_data = response.json()
        print(f"Successfully fetched {len(jobs_data)} job listings.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch job list: {e}")
        return
    except json.JSONDecodeError:
        print("Failed to decode JSON from job list. Response content:")
        print(response.text)
        return

    jobs = []
    script_start_time = time.time()
    
    print("\n--- Starting to process job data ---")
    for i, job_data_item in enumerate(jobs_data): # Renamed job_data to job_data_item
        if time.time() - script_start_time > SCRIPT_TIMEOUT_SECONDS:
            print(f"\n--- Script timed out after {SCRIPT_TIMEOUT_SECONDS // 60} minutes. Exiting. ---")
            break

        job_title = job_data_item.get("mos_title")
        job_code = job_data_item.get("moscode")
        job_category = job_data_item.get("category")
        
        # Get description directly from the initial JSON data
        description = job_data_item.get("MOS job overview", "N/A") 

        if not all([job_title, job_code, job_category]):
            print(f"  -> INFO: Skipping record {i+1} due to missing essential data.")
            continue

        job_sub_category = get_job_sub_category(job_category)
        sanitized_title = re.sub(r'[/,]', '', job_title.lower()).replace(' ', '-')
        job_url = f"{base_url}/careers-and-jobs/{job_category}/{job_sub_category}/{job_code.lower()}-{sanitized_title}"

        print(f"({i+1}/{len(jobs_data)}) Processing: {job_title}...")
        print(f"  -> URL: {job_url}") # Still useful for verification

        jobs.append({
            "title": job_title,
            "code": job_code,
            "category": job_category,
            "sub_category": job_sub_category,
            "url": job_url,
            "description": description
        })

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    print(f"\nScraping complete. {len(jobs)} jobs saved to jobs.json")

if __name__ == "__main__":
    main()
