import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_airforce_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Step 1: Fetch job data from the JSON API using Playwright
        jobs = []
        offset = 0
        total = 1
        
        while offset < total:
            api_url = f"https://www.airforce.com/bin/api/careers?careersRootPath=%2Fcontent%2Fairforce%2Fen%2Fcareers&limit=10&offset={offset}"
            print(f"Fetching job data from API: {api_url}")
            await page.goto(api_url, wait_until="load", timeout=60000)
            content = await page.content()
            
            # The response is HTML with a pre tag containing the JSON
            json_text = await page.locator('pre').inner_text()
            api_data = json.loads(json_text)
            
            if total == 1:
                total = api_data.get("pagination", {}).get("total")

            for item in api_data.get("data", []):
                title = item.get("title")
                link_obj = item.get("link")
                afsc_code = item.get("afscCode")
                if title and link_obj and link_obj.get("url"):
                    path = link_obj.get("url")
                    jobs.append({"title": title.strip(), "link": path, "jobCode": afsc_code})
            
            offset = len(jobs)

        print(f"Found {len(jobs)} jobs from API. Now extracting detailed descriptions...")

        # Step 2: Use Playwright to get detailed descriptions for each job
        for job in jobs:
            if job['link'] == "/careers/logistics-and-administration/behavioral-sciences-human-factors-scientist":
                print(f"Skipping broken link: {job['link']}")
                continue
            full_url = f"https://www.airforce.com{job['link']}"
            print(f"Navigating to detailed page for: {job['title']} ({full_url})")
            await page.goto(full_url, wait_until="load", timeout=60000)

            description_elements = await page.locator(".content-description").all_text_contents()
            card_items_elements = await page.locator(".card-items").all_text_contents()
            description_content = "\n".join([d.strip() for d in description_elements])
            card_items_content = "\n".join([c.strip() for c in card_items_elements])
            job['description'] = f"{description_content}\n\n{card_items_content}"

        await browser.close()

    # Save the collected data to a JSON file
    with open("airforce_jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)
    print("Data saved to airforce_jobs.json")
    print("Scraping complete.")

if __name__ == "__main__":
    asyncio.run(scrape_airforce_jobs())
