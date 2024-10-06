from src.scraper.CntrlScraper import CntrlScraper
from src.scraper.SptcScraper import SptcScraper

class CarDataProcessorFactory:
    @staticmethod
    def create_scraper(car_website):
        if car_website == "cntrl":
            return CntrlScraper()
        if car_website == "sptc":
            return SptcScraper()