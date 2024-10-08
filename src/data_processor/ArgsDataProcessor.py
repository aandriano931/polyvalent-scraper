from src.data_processor.CarDataProcessorFactory import CarDataProcessorFactory
from src.tool.Logger import Logger

class ArgsDataProcessor:
    @staticmethod
    def process_car_data(car_model):
        logger = Logger.get_logger(__name__)
        scraper = CarDataProcessorFactory.create_scraper('args')
        data_to_export = scraper.scrape_car_data(car_model)
        if data_to_export is not None:
            transformer = CarDataProcessorFactory.create_transformer('args')
            transformed_data = transformer.transform_collection(data_to_export)
            dao = CarDataProcessorFactory.create_dao()
            dao.insert_many(transformed_data)                    
        else:
            logger.info("Nothing to import.")