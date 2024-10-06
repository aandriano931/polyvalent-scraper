from src.data_processor.CarDataProcessorFactory import CarDataProcessorFactory
from src.tool.Logger import Logger

class SptcDataProcessor:
    @staticmethod
    def process_car_data(car_model):
        logger = Logger.get_logger(__name__)
        scraper = CarDataProcessorFactory.create_scraper('sptc')
        data_to_export = scraper.scrape_car_data(car_model)
        if data_to_export is not None:
            logger.info(data_to_export)                
        else:
            logger.info("Nothing to import.")