# Gemini Project Context

## Project Overview

This project is a web scraper written in Python. The goal is to scrape job data from the U.S. Army careers website: `https://www.goarmy.com/careers-and-jobs/browse-jobs`.

The website loads job data dynamically from a JSON file. However, the server has anti-scraping measures in place that block direct requests to this file.

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

The scraper first attempts to download a JSON file from `https://www.goarmy.com/careers-and-jobs/browse-jobs.jobs.json`. This file contains a list of all the jobs.

For each job in the JSON file, the scraper constructs a URL to the detailed job page. The URL has the following format:
`https://www.goarmy.com/careers-and-jobs/{jobCategory}/{jobSubCategory}/{jobCode}-{jobTitle}`

The `jobSubCategory` is determined by a mapping from the `jobCategory`.

The scraper then fetches the detailed job page and parses the HTML to extract the job description.

### Anti-Scraping Measures

The server blocks direct requests to the JSON file. The scraper attempts to bypass this by setting the `User-Agent` and `X-Requested-With` headers in the HTTP request.

**TODO:** The current implementation is still being blocked. A headless browser like Selenium or Puppeteer may be required to successfully scrape the data.