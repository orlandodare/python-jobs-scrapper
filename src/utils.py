import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def human_delay(min_s, max_s):
    """
    Pause the script diring a random delay where min_s is the minimum and max_s the maximum
    """
    wait = random.uniform(min_s, max_s)
    print(f" [Waiting {round(wait, 2)}s...]")
    time.sleep(wait)

def simulate_human_interaction(driver):
    """
    Simulate human behaviors (scrolls, mouse mouvements) to deceive Cloudflare-type detection systems.
    """
    
    try:
        actions = ActionChains(driver)

        # 1. Random mouse movement
        x = random.randint(10, 500)
        y = random.randint(10, 500)
        actions.move_by_offset(x, y).perform()

        # 2. Scroll whell imitation
        for  _ in range(random.randint(2,4)):
            step = random.randint(150, 400)
            driver.execute_script(f"window.scrollBy(0, {step});")
            human_delay(0.3, 0.8)

    except Exception:
        #Ignore if mouse go out of the window or if element not ready
        print("Something went wrong with the human simulate")
        pass

def got_to_next_page(driver):
    """
    Clik on the next page button
    """
    try:
        # Search for the next button
        next_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="pagination-page-next"]' )

        # 1. human scroll to the button
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
        human_delay(1.5, 3.0)

        # 2. click on the button
        next_button.click()
        print("Navigation vers la page suivante...")
        return True
    except Exception as e:
        print("Fin des pages ou bouton Suivant introuvable.")
        return False