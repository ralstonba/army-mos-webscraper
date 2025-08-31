# Gemini Project Context

## Project Overview

This project is a web scraper written in Python. The goal is to scrape job data from the U.S. Army careers website: `https://www.goarmy.com/careers-and-jobs/browse-jobs`.

We have found that the Army job data is available directly in a JSON file at `https://www.goarmy.com/careers-and-jobs/browse-jobs.jobs.json`. This file contains a list of job objects, each with `jobCategory`, `jobSubCategory`, `jobCode`, `jobTitle`, and `jobDescription`.

For Air Force jobs, the website `https://www.airforce.com/careers/career-finder` lists all jobs. We have determined that the job data is available via an API endpoint: `https://www.airforce.com/bin/api/careers?careersRootPath=%2Fcontent%2Fairforce%2Fen%2Fcareers`. This API provides job titles and relative links to detailed job pages. However, the full job descriptions are not directly available in this API response. Therefore, a headless browser (Playwright) is required to scrape the detailed job descriptions from individual job pages.

## Building and Running

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the scraper:**
    ```bash
    python scraper.py
    ```
    **Run the Air Force scraper:**
    ```bash
    python airforce_scraper.py
    ```

## Development Conventions

The project uses the `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML. For Air Force job scraping, `Playwright` is used for headless browser automation.

The main script for Army jobs is `scraper.py`. The main script for Air Force jobs is `airforce_scraper.py`.

### Scraping Logic

The Army scraper now directly downloads the `jobs.json` file. For each job in the JSON file, the scraper constructs a URL to the detailed job page. The URL has the following format:
`https://www.goarmy.com/careers-and-jobs/{jobCategory}/{jobSubCategory}/{jobCode}-{jobTitle}`

The `jobSubCategory` is determined by a mapping from the `jobCategory`.

The Army scraper extracts the job description directly from the initial JSON data.

For Air Force jobs, `airforce_scraper.py` first fetches data from the `https://www.airforce.com/bin/api/careers` API. It extracts job titles and relative links from this API. Then, it uses Playwright to navigate to each detailed job page (constructed using the base URL `https://www.airforce.com` and the relative link) to extract the full job description. The `airforce_jobs.json` file now contains absolute links for each job.

## To-Dos

*   **Error Handling and Robustness:** Implement more robust error handling and retry mechanisms for web requests and page navigation in `airforce_scraper.py`.
*   **Concurrency/Performance:** Explore implementing concurrency (e.g., using `asyncio.gather`) in `airforce_scraper.py` to speed up the scraping of multiple detailed job pages.
*   **Data Schema Consistency:** Consider unifying the data schema for Army and Air Force job data if they are to be combined or used together.
*   **Configuration:** Move hardcoded URLs, selectors, and other configurable parameters to a separate configuration file.
*   **Logging:** Replace `print` statements with a proper logging system for better debugging and monitoring.
*   **User-Agent and Headers:** Investigate more sophisticated User-Agent and header management for more robust scraping.
*   **Testing:** Write automated tests for both `scraper.py` and `airforce_scraper.py` to ensure future changes don't introduce regressions.