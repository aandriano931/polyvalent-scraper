import os
from src.tool.Base64ToolBox import Base64ToolBox as b64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class SeleniumBrowser:
    
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=chrome_options
        )
        self.prepare_browser()

    def prepare_browser(self):
        if self.browser.find_elements(By.ID, 'noVNC_connect_button'):
            self.login()

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
    

