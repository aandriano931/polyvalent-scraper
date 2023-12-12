from src.data_processor.BankDataProcessorFactory import BankDataProcessorFactory

class FortuneoDailyDataProcessor:
    @staticmethod
    def process_bank_data(banking_account):
        scraper = BankDataProcessorFactory.create_scraper(banking_account)
        data_to_export = scraper.scrap_account_daily_data()
        if data_to_export is not None:
            transformer = BankDataProcessorFactory.create_transformer(banking_account)
            transformed_data = transformer.transform_collection(data_to_export)
            dao = BankDataProcessorFactory.create_dao(banking_account)
            dao.insert_many(transformed_data)                
        else:
            print("Nothing to import.")