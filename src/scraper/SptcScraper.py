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


class SptcScraper:
    
    COROLLA_BASE_URL = os.getenv("SPTC_ENTRYPOINT_URL") + "/voitures-occasion?page=1&filters[0][brand]=toyota&filters[1][model]=corolla&filters[2][min_year]=2021"
    
    class NoTransactionsError(Exception):
        pass
    
    def __init__(self):
        browser = SeleniumBrowser()
        self.browser = browser.get_browser()
        self.wait = WebDriverWait(self.browser, 2)
        
    def scrape_car_data(self, car_type):
        try:
            logger = Logger.get_logger(__name__)
            if (car_type == "corolla"):
                base_url = self.COROLLA_BASE_URL            
            self.browser.get(base_url)
            self.handle_cookies_popup()
            logger.info("Scraping url : %s.", base_url)
            data = self.get_car_offers_data()
            offer_count = len(data)
            logger.info("Sptc car offers checked for car model : %s. %s results found.", car_type, offer_count)
            
            return data
        finally:
            self.browser.quit()
            
    def handle_cookies_popup(self):
        WebDriverWait(self.browser, 2)
        if self.browser.find_elements(By.ID, '_psaihm_main_div'):
            logger = Logger.get_logger(__name__)
            logger.info("Bypassing cookies popup.")
            privacy_button = self.browser.find_element(By.ID, '_psaihm_id_accept_all_btn')
            privacy_button.click()
                   
    def get_car_offers_data(self):
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        car_offers_result_container = soup.find('div', id="vo-results-search")
        if car_offers_result_container:
            car_offers_containers = car_offers_result_container.find_all('div', class_='reskin-product-card')
            car_data = []
            for offer_container in car_offers_containers:
                car_info = {}
                car_info['origin'] = 'sptc'
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                car_info['scraping_time'] = current_time
                car_internal_ref = offer_container.get('data-vo-id')
                car_info['internal_ref'] = car_internal_ref
                car_main_container = offer_container.find('div', class_='card')
                if car_main_container:
                    car_infos_container = car_main_container.find('div', class_='card-wrapper')
                    if car_infos_container:
                        car_href = car_infos_container.find('a').get('href')
                        car_content_container = car_infos_container.find('div', class_='card-content')
                        if car_content_container:
                            car_title = car_infos_container.find('span', class_='title').get_text(strip=True)
                            car_subtitle = car_infos_container.find('span', class_='sub-title').get_text(strip=True)
                            car_info.update({
                                'title': car_title,
                                'subtitle': car_subtitle,
                                'url': os.getenv("SPTC_ENTRYPOINT_URL") + car_href
                            })
                            mileage_container = car_content_container.find('div', class_='miles')
                            if mileage_container:
                                tags = mileage_container.find('ul', class_='tags').find_all('li')
                                mileage = tags[0].text.strip()
                                motorisation = tags[1].text.strip()
                                production_date = tags[2].text.strip()
                                gear_type = tags[3].text.strip()
                                car_info.update({
                                    'mileage': mileage,
                                    'motorisation': motorisation,
                                    'production_date': production_date,
                                    'gear_type': gear_type
                                })
                            price_container = car_content_container.find('div', class_='price-infos')
                            if price_container:
                                price = price_container.find('span').text.strip()
                                car_info['price'] = price
                                
                    address_container = car_main_container.find('div', class_='address-section')
                    if address_container:
                        localisation_retailspan = address_container.find('span', class_='localisation-retail')
                        if localisation_retailspan:
                            localisation_retail = localisation_retailspan.text.strip()
                            car_info['address'] = localisation_retail
                    
                car_data.append(car_info)
        else:
            raise NoOfferException("There wasn't any car offers.")

        return car_data
            