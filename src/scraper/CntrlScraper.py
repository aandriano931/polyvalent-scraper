import os, html, json
from src.exceptions.NoOfferException import NoOfferException
from src.tool.Base64ToolBox import Base64ToolBox as b64
from src.tool.SeleniumBrowser import SeleniumBrowser
from src.tool.Logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep


class CntrlScraper:
    
    COROLLA_BASE_URL = os.getenv("CNTRL_ENTRYPOINT_URL") + "/listing?energies=hyb&gearbox=AUTO&makesModelsCommercialNames=TOYOTA%3ACOROLLA"
    
    class NoTransactionsError(Exception):
        pass
    
    def __init__(self):
        browser = SeleniumBrowser()
        self.browser = browser.get_browser()
        self.wait = WebDriverWait(self.browser, 2)
        
    def scrape_car_data(self, car_type, url_parameters):
        try:
            logger = Logger.get_logger(__name__)
            if (car_type == "corolla"):
                base_url = self.COROLLA_BASE_URL
            if 'page' in url_parameters:
                page = url_parameters['page']
            else:
                page = 1
            if 'year_min' in url_parameters:
                year_min = url_parameters['year_min']
            else:
                year_min = 2022
            if 'mileage_min' in url_parameters:
                mileage_min = url_parameters['mileage_min']
            else:
                mileage_min = 1000
            
            url = "https://www.lacentrale.fr/"
            self.browser.get(url)
            logger.info("Connecting to : %s.", url)

            self.handle_cookies_popup()
            scraping_url = f"{base_url}&page={page}&year_min={year_min}&mileage_min={mileage_min}"
            logger.info("Scraping url : %s.", scraping_url)
            self.browser.get(scraping_url)

            data = self.get_car_offers_data()
            offer_count = len(data)
            logger.info("Ctrnl car offers checked for car model : %s. %s results found.", car_type, offer_count)
            
            return data
        finally:
            self.browser.quit()
            
    def handle_cookies_popup(self):
        WebDriverWait(self.browser, 5)
        
        if self.browser.find_elements(By.ID, 'didomi-popup'):
            logger = Logger.get_logger(__name__)
            logger.info("Bypassing cookies popup.")
            privacy_button = self.browser.find_element(By.ID, 'didomi-notice-agree-button')
            privacy_button.click()
                   
    def get_car_offers_data(self):
        page_source = self.browser.page_source
        logger = Logger.get_logger(__name__)
        soup = BeautifulSoup(page_source, 'html.parser')
        logger.info(soup)

        car_offers_result_container = soup.find('div', class_="searchCardContainer")
        if car_offers_result_container:
            car_offers_containers = car_offers_result_container.find_all('div', class_='searchCard')
            car_data = []
            for offer_container in car_offers_containers:
                car_data.append['origin' : 'cntrl']
                car_info = []
                data_tracking_meta = offer_container.get('data-tracking-meta')
                if data_tracking_meta:
                    decoded_meta = html.unescape(data_tracking_meta)
                    meta_dict = json.loads(decoded_meta)
                    owner_category = meta_dict.get('owner_category')
                    classified_ref = meta_dict.get('classified_ref')
                    car_info.append({
                        'category': owner_category,
                        'internal_ref': classified_ref
                    })
                car_a_container = offer_container.find('a')
                if car_a_container:
                    car_url = car_a_container.get('href')
                    car_info.append({'url': car_url})
                    car_infos_container = car_a_container.find('div', class_=lambda x: x and 'informationsContainer' in x)
                    if car_infos_container:
                        car_info.append({
                            'label': car_infos_container.find('h2').get_text(strip=True),
                            'sub_label': car_infos_container.find('div', class_=lambda x: x and 'subTitle' in x).get_text(strip=True),
                        })
                        car_characteristics_main_container = car_infos_container.find('div', class_=lambda x: x and 'vehicleCharacteristics' in x)
                        if car_characteristics_main_container:
                            car_characteristics_containers = car_characteristics_main_container.find_all('div', class_=lambda x: x and 'vehicleCharacteristicsItem' in x)
                            if len(car_characteristics_containers) != 4:
                                raise ValueError("Expected exactly 4 characteristic divs, but found {}".format(len(car_characteristics_containers)))
                            car_info.append({
                            'year': car_characteristics_containers[0].find('div').get_text(strip=True),
                            'transmission': car_characteristics_containers[1].find('div').get_text(strip=True),
                            'mileage': car_characteristics_containers[2].find('div').get_text(strip=True),
                            'motorisation': car_characteristics_containers[3].find('div').get_text(strip=True)
                            })

                car_data.append(car_info)
        else:
            raise NoOfferException("There wasn't any car offers.")

        return car_data
            