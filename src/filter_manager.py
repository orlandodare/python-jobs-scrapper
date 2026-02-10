
def is_job_relevant(job_title, config):
    """
    Checks if a job title matches the user's criteria.
    Logic: Exclude first, then Include.
    """
    title = job_title.lower()

    # Gets filters with default empty lists to avoid crashes
    title_filters = config.get('title_filters', {})
    excluded_words = title_filters.get('excluded', [])
    keywords = title_filters.get('keywords', [])

    # 1. Exclusion (Highest priority)
    for word in excluded_words:
        if word.lower() in title:
            return False
            
    # 2. Inclusion
    for word in keywords:
        if word.lower() in title:

            # Helps the user to see WHY a job was picked
            print(f"  -> Match found: '{word}' in '{job_title}'")
            return True
        
    return False

def job_check_new(jobs_found, known_urls, config):
    """
    Separates truly new jobs from known ones and filters them by relevance.
    """
    new_jobs=[]
    relevant_jobs=[]

    for job in jobs_found:
        #Checks if we've seen this URL before
        if job['url'] not in known_urls:
            new_jobs.append(job)

            #If it's new, checks if the job is interesting
            if is_job_relevant(job['title'], config):
                relevant_jobs.append(job)
                
    return relevant_jobs, new_jobs



