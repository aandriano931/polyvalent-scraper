from src.scraper.SptcScraper import SptcScraper
from src.scraper.ArgsScraper import ArgsScraper
from src.data_transformer.SptcDataTransformer import SptcDataTransformer
from src.data_transformer.ArgsDataTransformer import ArgsDataTransformer
from src.dao.CarOfferDAO import CarOfferDAO

class CarDataProcessorFactory:
    @staticmethod
    def create_scraper(car_website):
        if car_website == "sptc":
            return SptcScraper()
        if car_website == "args":
            return ArgsScraper()
    
    @staticmethod
    def create_transformer(website):
        if website == "sptc":
            return SptcDataTransformer()
        if website == "args":
            return ArgsDataTransformer()
        # Add more cases for other transformers if needed

    @staticmethod
    def create_dao():
        return CarOfferDAO()