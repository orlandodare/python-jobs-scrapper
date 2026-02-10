from selenium.webdriver.common.by import By
import time
import random


def extract_jobs_from_page(driver):
    """
    Scans the current Indeed page and extracts job titles, URLs and companies
    """
    # 1. Behavior: Random human-like delays
    wait_time = random.uniform(8.5, 15.2)
    print(f"Security wait : {round(wait_time, 2)} seconds...")
    time.sleep(wait_time)

    # 2. Behavior: Random scroll to trigger lazy loading
    pixel_scroll = random.randint(300, 700)
    driver.execute_script(f"window.scrollTo(0, {pixel_scroll});")
    time.sleep(random.uniform(1.0, 2.0))
    
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