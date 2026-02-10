from selenium.webdriver.common.by import By
import time
import random
from src.utils import human_delay, simulate_human_interaction


def extract_jobs_from_page(driver):
    """
    Scans the current Indeed page and extracts job titles, URLs and companies
    """
    # 1. Behavior: Random human-like delays
    human_delay(8.5, 15.2)

    # 2. Behavior: Random scroll and mouse movement to trigger lazy loading
    simulate_human_interaction(driver)
    
    jobs_found = []

    # Indeed often wraps jobs in this container
    offers = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

    for offer in offers:
        try:
            title = offer.find_element(By.CSS_SELECTOR, "h2.jobTitle span[id*='jobTitle']").text.strip()
            url = offer.find_element(By.CSS_SELECTOR, "h2.jobTitle a").get_attribute('href')
            company = offer.find_element(By.CSS_SELECTOR, "[data-testid*='company']").text.strip()
            #Save the job in the list
            jobs_found.append({
                "title": title,
                "url": url,
                "company": company
            })
        except Exception:
            # Silently skip if a specific element is missing (e.g., ad, layout change)
            continue
    
    print(f"Successfully extracted {len(jobs_found)} jobs from this page.")

    return jobs_found