
import undetected_chromedriver as uc
from selenium_stealth import stealth




def get_driver():
    """
    Initializes and returns customized undetected-chromedriver with stealth settings.
    """
    
    options = uc.ChromeOptions()

    # Standard anti-detection arguments
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Initializes driver (auto-detects Chrome version for better portability)
    driver = uc.Chrome(options=options, version_main=144)
    

    # Selenium-Stealth : Deep masking of browser fingerprints
    stealth(driver,
            languages=["fr-FR", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    # Implicit wait: gives the page a bit of time to load elements
    driver.implicitly_wait(5)
    
    return driver