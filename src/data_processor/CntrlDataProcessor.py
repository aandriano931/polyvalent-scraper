from src.data_processor.CarDataProcessorFactory import CarDataProcessorFactory
from src.tool.Logger import Logger

class CntrlDataProcessor:
    @staticmethod
    def process_car_data(car_model, parameters):
        logger = Logger.get_logger(__name__)
        scraper = CarDataProcessorFactory.create_scraper('cntrl')
        data_to_export = scraper.scrape_car_data(car_model, parameters)
        if data_to_export is not None:
            logger.info(data_to_export)                
        else:
            logger.info("Nothing to import.")