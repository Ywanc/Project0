from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Set up the WebDriver

driver = webdriver.Chrome()

# URL of the page to scrape
url = 'https://www.judiciary.gov.sg/judgments/judgments-case-summaries'
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # You can adjust the wait time if necessary

# Find all links to judgments (adjust the selector as needed)
judgment_links = driver.find_elements(By.TAG_NAME, 'a')
# Extract and print the links
for link in judgment_links:
    href = link.get_attribute('href')
    # Check if the link is a judgment link
    if "judgment" in href:
        print(href)

# Close the driver
driver.quit()
