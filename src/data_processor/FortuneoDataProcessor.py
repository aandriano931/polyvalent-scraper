from src.data_processor.BankDataProcessorFactory import BankDataProcessorFactory
from src.tool.Logger import Logger

class FortuneoDataProcessor:
    @staticmethod
    def process_bank_data(banking_account, date_delta):
        logger = Logger.get_logger()
        scraper = BankDataProcessorFactory.create_scraper(banking_account)
        data_to_export = scraper.scrape_account_data(date_delta)
        if data_to_export is not None:
            transformer = BankDataProcessorFactory.create_transformer(banking_account)
            transformed_data = transformer.transform_collection(data_to_export)
            dao = BankDataProcessorFactory.create_dao(banking_account)
            dao.insert_many(transformed_data)                
        else:
            logger.info("Nothing to import.")