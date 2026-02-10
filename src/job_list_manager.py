from pathlib import Path
import pandas as pd
import csv

def load_known_urls(file_path):
    """
    Load existing job URLs from a CSV file into a set for fast lookup
    """
    job_Set = set()
    path = Path(file_path)
    if path.exists() and path.stat().st_size >0:
        try:
            # Explicit encoding to handle accent properly
            df=pd.read_csv(file_path, encoding="utf-8")
            if 'url' in df.columns:
                job_set = set(df['url'].dropna())
        except Exception as e:
            print(f"Warning: Could not read {file_path}. Starting with empty set. Error: {e}")

    return job_Set


def save_jobs(file_path, jobs_to_save):
        """
        Appends a list of job dictionaries to a CSV file. 
        Creates the file and header if it doesn't exist.
        """
        if not jobs_to_save :
            return
        
        path = Path(file_path)

        # Ensure the directory (data/) exists
        path.parent.mkdir(parents=True, exist_ok=True)

        file_exists = path.exists() and path.stat().st_size > 0

        # We define the columns based on the first job's keys to be generic
        fieldnames = jobs_to_save[0].keys()

        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #We check if the file is new or not to write header only ones
            if not file_exists:
                writer.writeheader()

            writer.writerows(jobs_to_save)
            
        print(f"Saved {len(jobs_to_save)} jobs to {file_path}")
    