from src.dao.BankTransactionDAO import BankTransactionDAO
from src.data_transformer.FtnDataTransformer import FtnDataTransformer
from src.scraper.FtnScraper import FtnScraper

class BankDataProcessorFactory:
    @staticmethod
    def create_scraper(banking_account):
        if banking_account == "joint_account":
            return FtnScraper("joint_account")
        if banking_account == "personal_account":
            return FtnScraper("personal_account")
        # Add more cases for other banking accounts if needed

    @staticmethod
    def create_transformer(banking_account):
        if banking_account == "joint_account" or banking_account == "personal_account":
            return FtnDataTransformer()
        # Add more cases for other transformers if needed

    @staticmethod
    def create_dao(banking_account):
        # Return the appropriate DAO based on the collection name
        if banking_account == "joint_account":
            return BankTransactionDAO("ftn_joint_account")
        if banking_account == "personal_account":
            return BankTransactionDAO("ftn_personal_account")
        # Add more cases for other DAOs if needed
