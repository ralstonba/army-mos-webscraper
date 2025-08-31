import asyncio
from playwright.async_api import async_playwright

async def scrape_airforce_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Navigating to Air Force career finder page...")
        await page.goto("https://www.airforce.com/careers/career-finder")
        print("Page loaded.")

        jobs = []
        job_elements = await page.locator(".search-item .name").all()
        for job_element in job_elements:
            title = await job_element.text_content()
            link = await job_element.get_attribute("href")
            if title and link:
                jobs.append({"title": title.strip(), "link": link})
                print(f"Found job: {title.strip()} - {link}")

        print(f"Found {len(jobs)} jobs. Now extracting detailed descriptions...")

        for job in jobs:
            print(f"Navigating to detailed page for: {job['title']}")
            await page.goto(f"https://www.airforce.com{job['link']}")

            description_elements = await page.locator(".content-description").all_text_contents()
            card_items_elements = await page.locator(".card-items").all_text_contents()
            description_content = "\n".join([d.strip() for d in description_elements])
            card_items_content = "\n".join([c.strip() for c in card_items_elements])
            job['description'] = f"{description_content}\n\n{card_items_content}"
            print(f"Description for {job['title']}: {job['description'][:100]}...") # Print first 100 chars

        import json
        with open("airforce_jobs.json", "w") as f:
            json.dump(jobs, f, indent=4)
        print("Data saved to airforce_jobs.json")

        await browser.close()
        print("Scraping complete.")

if __name__ == "__main__":
    asyncio.run(scrape_airforce_jobs())
