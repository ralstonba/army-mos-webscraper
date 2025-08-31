# Gemini Project Context

## Project Overview

This project is a web scraper written in Python. The goal is to scrape job data from the U.S. Army careers website: `https://www.goarmy.com/careers-and-jobs/browse-jobs`.

We have found that the Army job data is available directly in a JSON file at `https://www.goarmy.com/careers-and-jobs/browse-jobs.jobs.json`. This file contains a list of job objects, each with `jobCategory`, `jobSubCategory`, `jobCode`, `jobTitle`, and `jobDescription`.

For Air Force jobs, the website `https://www.airforce.com/careers/career-finder` lists all jobs. However, we have determined that the job data is not available in a direct JSON file and is likely loaded dynamically. Therefore, a headless browser (like Selenium or Puppeteer) will be required to scrape this data.

## Building and Running

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the scraper:**
    ```bash
    python scraper.py
    ```

## Development Conventions

The project uses the `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML.

The main script is `scraper.py`.

### Scraping Logic

The Army scraper now directly downloads the `jobs.json` file. For each job in the JSON file, the scraper constructs a URL to the detailed job page. The URL has the following format:
`https://www.goarmy.com/careers-and-jobs/{jobCategory}/{jobSubCategory}/{jobCode}-{jobTitle}`

The `jobSubCategory` is determined by a mapping from the `jobCategory`.

The scraper then fetches the detailed job page and parses the HTML to extract the job description.