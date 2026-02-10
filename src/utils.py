import random
import time
from selenium.webdriver.common.action_chains import ActionChains

def human_delay(min_s, max_s):
    """
    Pause the script diring a random delay where min_s is the minimum and max_s the maximum
    """
    wait = random.uniform(min_s, max_s)
    print(f" [Waitin {round(wait, 2)}s...]")
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
            step = random.radint(150, 400)
            driver.execute_script(f"windows.scrollBy(0, {step});")
            human_delay(0.3, 0.8)

    except Exception:
        #Ignore if mouse go out of the window or if element not ready
        pass

