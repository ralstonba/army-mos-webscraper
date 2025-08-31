import asyncio
import requests
import json
from playwright.async_api import async_playwright

async def scrape_airforce_jobs():
    # Step 1: Fetch job data from the JSON API
    api_url = "https://www.airforce.com/bin/api/careers?careersRootPath=%2Fcontent%2Fairforce%2Fen%2Fcareers&limit=1000" # Increased limit to get all jobs
    print(f"Fetching job data from API: {api_url}")
    response = requests.get(api_url)
    response.raise_for_status() # Raise an exception for HTTP errors
    api_data = response.json()

    jobs = []
    for item in api_data.get("data", []):
        # Assuming the API returns title and path directly
        title = item.get("title")
        link_obj = item.get("link")
        if title and link_obj and link_obj.get("url"):
            path = link_obj.get("url")
            jobs.append({"title": title.strip(), "link": path})

    print(f"Found {len(jobs)} jobs from API. Now extracting detailed descriptions...")

    # Step 2: Use Playwright to get detailed descriptions for each job
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for job in jobs:
            full_url = f"https://www.airforce.com{job['link']}"
            print(f"Navigating to detailed page for: {job['title']} ({full_url})")
            await page.goto(full_url, wait_until="domcontentloaded")

            description_elements = await page.locator(".content-description").all_text_contents()
            card_items_elements = await page.locator(".card-items").all_text_contents()
            description_content = "\n".join([d.strip() for d in description_elements])
            card_items_content = "\n".join([c.strip() for c in card_items_elements])
            job['description'] = f"{description_content}\n\n{card_items_content}"
            # print(f"Description for {job['title']}: {job['description'][:100]}...") # Print first 100 chars

        await browser.close()

    # Save the collected data to a JSON file
    with open("airforce_jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)
    print("Data saved to airforce_jobs.json")
    print("Scraping complete.")

if __name__ == "__main__":
    asyncio.run(scrape_airforce_jobs())

        
