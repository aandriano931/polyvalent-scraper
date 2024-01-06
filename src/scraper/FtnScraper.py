import os
from src.tool.Base64ToolBox import Base64ToolBox as b64
from src.tool.SeleniumBrowser import SeleniumBrowser
from src.tool.Logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep

class FtnScraper:
    
    ENTRYPOINT_URL = os.getenv("FT_ENTRYPOINT_URL")
    ACCOUNTS_LINKS = {
        "joint_account" : os.getenv("FT_JOINT_ACC_ID"),
        "personal_account" : os.getenv("FT_PERSO_ACC_ID"),
    }
    
    def __init__(self, banking_account):
        browser = SeleniumBrowser()
        self.browser = browser.get_browser()
        self.browser.get(self.ENTRYPOINT_URL)
        self.banking_account = banking_account
        self.wait = WebDriverWait(self.browser, 2)
        
    def scrape_account_data(self, date_delta):
        try:
            logger = Logger.get_logger(__name__)
            self.handle_cookies_popup()
            self.login()
            self.display_account(self.banking_account)
            start_date = (datetime.now() - timedelta(days=date_delta)).strftime("%d/%m/%Y")
            end_date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
            self.display_account_events_by_dates(start_date, end_date)
            data = self.get_account_events_data()
            logger.info("Ftn banking events scraped for the last %s day(s): %s for account: %s", date_delta, data, self.banking_account)
            return data
        finally:
            self.browser.quit()
            
    def handle_cookies_popup(self):
        sleep(2)
        if self.browser.find_elements(By.ID, 'popin_tc_privacy_button_2'):
            privacy_button = self.browser.find_element(By.ID, 'popin_tc_privacy_button_2')
            privacy_button.click()
            
    def login(self):
        username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginContainer']/input[1]")))
        username_input.send_keys(b64.decode(os.getenv("FT_USERNAME")))
        password_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='passwordContainer']/span[1]/input")))
        password_input.send_keys(b64.decode(os.getenv("FT_PASSWORD")))
        connect_button = self.browser.find_element(By.ID, 'valider_login')
        connect_button.click()
        sleep(5)
        
    def display_account(self, account_name):
        account_link = self.wait.until(EC.element_to_be_clickable((By.ID, self.ACCOUNTS_LINKS[account_name])))
        account_link.click()
        
    def display_account_events_by_dates(self, start_date, end_date):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframe_centrale")))
        sleep(2)
        start_date_input = self.browser.find_element(By.CSS_SELECTOR, "input[name='dateRechercheDebut']")
        start_date_input.clear()
        start_date_input.send_keys(start_date)
        end_date_input = self.browser.find_element(By.CSS_SELECTOR, "input[name='dateRechercheFin']")
        end_date_input.clear()
        end_date_input.send_keys(end_date)
        date_selection_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ongletSolde']/div[2]/a")))
        date_selection_link.click()
        sleep(2)
        self.browser.switch_to.default_content()
        
    def get_account_events_data(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframe_centrale")))
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        events_tab = soup.find('table', id="tabHistoriqueOperations")
        if events_tab:
            # Do not keep headers
            rows = events_tab.find_all('tr')[1:]
            table_data = []
            for row in rows:
                cells = row.find_all(['th', 'td'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                table_data.append(row_data)
            
            self.browser.switch_to.default_content()
            return table_data
        else:
            raise ValueError("Could not find table with banking data")
    
            