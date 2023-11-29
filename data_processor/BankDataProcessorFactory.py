from dao.BankTransactionDAO import BankTransactionDAO
from data_transformer.FortuneoDataTransformer import FortuneoDataTransformer
from scraper.FortuneoScraper import FortuneoScraper

class BankDataProcessorFactory:
    @staticmethod
    def create_scraper(banking_account):
        if banking_account == "joint_account":
            return FortuneoScraper("joint_account")
        if banking_account == "personal_account":
            return FortuneoScraper("personal_account")
        # Add more cases for other banking accounts if needed

    @staticmethod
    def create_transformer(banking_account):
        if banking_account == "joint_account" or banking_account == "personal_account":
            return FortuneoDataTransformer()
        # Add more cases for other transformers if needed

    @staticmethod
    def create_dao(banking_account):
        # Return the appropriate DAO based on the collection name
        if banking_account == "joint_account":
            return BankTransactionDAO("fortuneo_joint_account")
        if banking_account == "personal_account":
            return BankTransactionDAO("fortuneo_personal_account")
        # Add more cases for other DAOs if needed
