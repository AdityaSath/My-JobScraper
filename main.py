from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

# Base URL for company job listings
base_url = 'https://www.bain.com/careers/find-a-role/'
# http get request to website
result = requests.get(base_url)
# create BeautifulSoup object to read the html of the file
bs = BeautifulSoup(result.text, "html.parser")

def pull_company_name(base_url, all_links, job_links):
    """
    Extracts job links from the company careers page.

    Parameters:
    base_url (str): The base URL of the company careers page.
    all_links (list): List of all links on the current page.
    job_links (list): List of collected job links.

    Returns:
    list: Updated list of job links.
    """

    for link in all_links:
        # Append the link to job_links if it meets the criteria
        for link in all_links:
            # Pattern: all job posts have href att starting with "/careers/find-a-role/position/?jobid="
            if(link['href'].startswith('/careers/find-a-role/position/?jobid=')):
                # concatenate bain.com to the link to get full https link
                job_links.append("https://www.bain.com/" + link['href'])
    # Full list of jobs
    return job_links

def button_company_name(driver, page, outer_loop_break, all_links):
    """
    Handles pagination by clicking the "next page"/"load more" button.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    page (int): The current page number. (optional)
    outer_loop_break (bool): Flag to indicate when to stop scraping.
    all_links (list): List of all links on the current page.

    Returns:
    tuple: Updated page number and outer_loop_break flag.
    """
    try:
        # Locate the next page button and navigate to the next page if it exists
        # pattern: load more button has class name: btn btn--cta, so find it
        next = bs.find('a', class_="btn btn--cta")
        # Simulate clicking load more button
        next.click()
        # provide timeout to ensure results load before continuing
        time.sleep(5)

        pass
    except Exception as e:
        print(f"Error occurred while trying to click the 'next page' button: {e}")
        outer_loop_break = True
    return page + 1, outer_loop_break

# WebDriver setup
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(base_url)

# Initialize variables
job_links = []
prev_page = 0
page = 1

# Main scraping loop
while True:
    time.sleep(5)
    outer_loop_break = False
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    all_links = soup.find_all("a", href=True)

    # Scrape job links
    job_links = pull_company_name(base_url, all_links, job_links)

    # Handle pagination
    page, outer_loop_break = button_company_name(driver, page, outer_loop_break, all_links)

    if outer_loop_break:
        break

# Output the collected job links
print("Collected job links:", job_links)

# Close the WebDriver
driver.quit()
