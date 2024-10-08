import os
from src.exceptions.NoOfferException import NoOfferException
from src.tool.SeleniumBrowser import SeleniumBrowser
from src.tool.Logger import Logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime


class ArgsScraper:
    
    COROLLA_BASE_URL = os.getenv("ARGS_ENTRYPOINT_URL") + "/auto/toyota/corolla/?energy=hybride&npp=30&year%5Bmin%5D=2021"
        
    def __init__(self):
        browser = SeleniumBrowser()
        self.browser = browser.get_browser()
        self.wait = WebDriverWait(self.browser, 2)
        
    def scrape_car_data(self, car_type):
        try:
            logger = Logger.get_logger(__name__)
            if (car_type == "corolla"):
                base_url = self.COROLLA_BASE_URL
                self.car_type = car_type
            self.browser.get(base_url)
            self.handle_cookies_popup()
            data = self.get_car_offers_data()
            offer_count = len(data)
            logger.info("Args car offers checked for car model : %s. %s results found.", car_type, offer_count)
            return data
        except Exception as e:
            logger.error("An error occurred while scraping car data: %s", str(e))
            raise
        finally:
            self.browser.quit()
            
    def handle_cookies_popup(self):
        WebDriverWait(self.browser, 2)
        if self.browser.find_elements(By.ID, 'didomi-popup'):
            logger = Logger.get_logger(__name__)
            logger.info("Bypassing cookies popup.")
            privacy_button = self.browser.find_element(By.ID, 'didomi-notice-agree-button')
            privacy_button.click()
                   
    def get_car_offers_data(self):
        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print(soup)
        exit()
        car_offers_result_container = soup.find('div', class_="list-group")
        if car_offers_result_container:
            car_offers_containers = car_offers_result_container.find_all('div', class_='list-group-item')
            car_data = []
            for offer_container in car_offers_containers:
                car_info = self.extract_car_info(offer_container)
                car_data.append(car_info)
        else:
            raise NoOfferException("There wasn't any car offers.")
        return car_data

    def extract_car_info(self, offer_container):
        car_info = {}
        car_info['origin'] = 'args'
        car_info['type'] = self.car_type
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        car_info['scraping_time'] = current_time
        car_internal_ref = offer_container.get('data-annonceid')
        car_info['internal_ref'] = car_internal_ref
        car_href = offer_container.find('a').get('href')
        car_info['url'] = os.getenv("SPTC_ENTRYPOINT_URL") + car_href
        car_main_container = offer_container.find('div', class_='row')
        if car_main_container:
            car_price_container = car_main_container.find('div', class_='price-container')
            if car_price_container:
                price = car_price_container.find('span', class_='prix').text.strip().replace('€', '').replace(' ', '')
                car_info['price'] = int(price)
            car_infos_container = car_main_container.find('div', class_='bottom')
            if car_infos_container:
                motorisation = car_infos_container.find('li', class_='energie').text.strip().replace('\xa0', '')
                mileage = car_infos_container.find('li', class_='km').text.strip().replace('\xa0', '')
                production_date = car_infos_container.find('li', class_='annee').text.strip().replace('\xa0', '')
                address = car_infos_container.find('li', class_='dept zipcode').text.strip().replace('\xa0', '')
                car_info.update({
                    'motorisation': motorisation,
                    'mileage': mileage,
                    'production_date': production_date,
                    'address': address
                })
            car_info['title'] = car_main_container.find('h3', class_='title-model').text.strip()
            version_span = car_main_container.find('span', class_='version')
            if version_span:
                car_info['subtitle'] = version_span.text.strip()

        return car_info