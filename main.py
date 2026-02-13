from src.browser_factory import get_driver
from src.job_list_manager import load_known_urls, save_jobs
from src.scraper_indeed import extract_jobs_from_page
from src.filter_manager import job_check_new
from src.utils import human_delay, simulate_human_interaction, got_to_next_page
import json
import os


def load_config():
    """Loads configuration from JSON file."""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def main():
    config = load_config()

    # Setup file paths
    file_path_all_jobs = os.path.join("data", "jobs_list.csv")
    file_path_relevant_jobs = os.path.join("data", "relevant_jobs_list.csv")

    # Load history to avoid duplicates
    jobs_set = load_known_urls(file_path_all_jobs)

    # Initialize the undetected-chromedriver
    driver = get_driver()

    #change_page=0
    count_page = 1
    consecutive_duplicates = 0

    try:
        # Loop until we encouter too many already saved jobs
        while consecutive_duplicates <5:
            print(f"Scraping Indeed page {count_page}...")
            #url = f"https://be.indeed.com/jobs?q=&l=Li%C3%A8ge&sort=date&start={change_page}"
            url = "https://be.indeed.com/jobs?q=&l=Li%C3%A8ge&radius=25&sort=date&vjk=ee6664542e8ad980"

           # if change_page > 0:
                # Add a referer
               # driver.execute_script(f"window.location.href = 'https://be.indeed.com/jobs?q=&l=Li%C3%A8ge&sort=date&start={change_page-10}';")

            driver.get(url)
            
            # Load all the jobs available from the page
            jobs_found = extract_jobs_from_page(driver)


            # Check if jobs are found otherwise stop the loop
            if not jobs_found:
                print("No jobs found or blocked by Cloudflare.")
                break
            
            simulate_human_interaction(driver)

            # Filter logic : keeps only new and relevant jobs based on criteria written in config.json
            relevant_jobs, new_jobs = job_check_new(jobs_found, jobs_set, config)

            
            
            if new_jobs:
                # If there are relevant jobs, saves them in a CSV
                if relevant_jobs:
                    save_jobs(file_path_relevant_jobs, relevant_jobs)
                    print(f"Found {len(relevant_jobs)} RELEVANT jobs!")

                # Update local set to avoid re-processing the same job in the same session
                for job in new_jobs:
                    jobs_set.add(job['url'])

                # Saves new jobs in the CSV file for the next time
                save_jobs(file_path_all_jobs, new_jobs)
                
            #Calculate how many jobs on this page were already in our database (if there is more than 4 we can consider that the other pages will contains already encoutered offers and stop the loop)
            consecutive_duplicates = len(jobs_found) - len(new_jobs)
            count_page+=1
            input("Appuie sur enter quand tu es prêt")
            got_to_next_page(driver)
            human_delay(10, 25)

    except Exception as e :
        print(f"An error as occurred: {e}")
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()

