import os
from src.tool.Base64ToolBox import Base64ToolBox as b64
from src.tool.Logger import Logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from time import sleep

class SeleniumBrowser:
    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(options=chrome_options)

        # self.browser = webdriver.Remote(
        #     command_executor='http://selenium:4444/wd/hub',
        #     options=chrome_options
        # )
        self.prepare_browser()

    def prepare_browser(self):
        logger = Logger.get_logger(__name__)
        try:
            stealth(self.browser,
                    languages=["fr-FR", "fr"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    )
            if self.browser.find_elements(By.ID, 'noVNC_connect_button'):
                self.login()
        except Exception as e:
            logger.error(f"Error preparing browser: {e}")
                
    def login(self):
        wait = WebDriverWait(self.browser, 2)
        connect_button = wait.until(EC.presence_of_element_located((By.ID, "noVNC_connect_button")))
        connect_button.click()
        self.browser.switch_to.alert
        password_input = wait.until(EC.element_to_be_clickable((By.ID, "noVNC_password_input")))
        password_input.send_keys(b64.decode(os.getenv("SELENIUM_PASSWORD")))
        send_button = wait.until(EC.element_to_be_clickable((By.ID, "noVNC_credentials_button")))
        send_button.click()
        sleep(2)
    
    def get_browser(self):
        return self.browser
    

