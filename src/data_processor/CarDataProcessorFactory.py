from src.scraper.CntrlScraper import CntrlScraper
from src.scraper.SptcScraper import SptcScraper
from src.data_transformer.SptcDataTransformer import SptcDataTransformer
from src.dao.CarOfferDAO import CarOfferDAO

class CarDataProcessorFactory:
    @staticmethod
    def create_scraper(car_website):
        if car_website == "cntrl":
            return CntrlScraper()
        if car_website == "sptc":
            return SptcScraper()
    
    @staticmethod
    def create_transformer(website):
        if website == "sptc":
            return SptcDataTransformer()
        # Add more cases for other transformers if needed

    @staticmethod
    def create_dao():
        return CarOfferDAO()