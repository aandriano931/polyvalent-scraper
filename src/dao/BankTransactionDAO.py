from src.dao.MysqlDAO import MysqlDAO
from src.dao.BankAccountDAO import BankAccountDAO
from src.tool.Logger import Logger

import uuid

class BankTransactionDAO(MysqlDAO):
    
    def __init__(self, bank_account_alias):
        self.table = 'bank_transaction'
        self.bank_account_alias = bank_account_alias
        super().__init__()
    
    def insert_one(self, dto_object):
        logger = Logger.get_logger(__name__)
        bank_account_dao = BankAccountDAO()
        bank_account_id = bank_account_dao.get_one_by_alias(self.bank_account_alias)
        cursor = self.mysql_connection.cursor()
        add_transaction_query = ("INSERT INTO {} "
               "(id, credit, debit, label, operation_date, value_date, bank_account_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)".format(self.table))
        
        new_uuid = str(uuid.uuid4())
        if dto_object.transaction_type == 'credit':
            credit = dto_object.amount
            debit = None
        else:
            credit = None
            debit = dto_object.amount    
        label = dto_object.label
        operation_date = dto_object.operation_date.strftime("%Y-%m-%d")
        value_date = dto_object.value_date.strftime("%Y-%m-%d")
        add_transaction_parameters = (new_uuid, credit, debit, label, operation_date, value_date, bank_account_id)
        cursor.execute(add_transaction_query, add_transaction_parameters)
        inserted_id = str(new_uuid)
        self.commit()
        cursor.close()
        self.close_connection()
        logger.info(f"Inserted one bank transaction with ID: {inserted_id}")
        return inserted_id
    
    def insert_many(self, dto_collection):
        logger = Logger.get_logger(__name__)
        bank_account_dao = BankAccountDAO()
        bank_account_id = bank_account_dao.get_one_by_alias(self.bank_account_alias)
        cursor = self.mysql_connection.cursor()
        inserted_ids = []
        for dto_object in dto_collection:
            add_transaction_query = ("INSERT INTO {} "
               "(id, credit, debit, label, operation_date, value_date, bank_account_id) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)".format(self.table))
            new_uuid = str(uuid.uuid4())
            if dto_object.transaction_type == 'credit':
                credit = dto_object.amount
                debit = None
            else:
                credit = None
                debit = dto_object.amount    
            label = dto_object.label
            operation_date = dto_object.operation_date.strftime("%Y-%m-%d")
            value_date = dto_object.value_date.strftime("%Y-%m-%d")
            add_transaction_parameters = (new_uuid, credit, debit, label, operation_date, value_date, bank_account_id)
            cursor.execute(add_transaction_query, add_transaction_parameters)
            inserted_ids.append(new_uuid)
        self.commit()
        cursor.close()
        self.close_connection()
        logger.info(f"Inserted {len(inserted_ids)} bank transactions with IDs: {inserted_ids}")
        return inserted_ids
    
    def get_all(self, categorized):
        logger = Logger.get_logger(__name__)
        cursor = self.mysql_connection.cursor()
        get_all_categorized_transactions_query = ("SELECT bank_transaction.id, operation_date, label, debit, credit, bank_category_id, bank_category.name FROM {} INNER JOIN bank_category ON bank_category.id = bank_transaction.bank_category_id ORDER BY operation_date ASC".format(self.table))
        get_non_categorized_transactions_query = ("SELECT bank_transaction.id, operation_date, label, debit, credit FROM {} WHERE bank_category_id IS NULL ORDER BY operation_date ASC".format(self.table))
        if categorized == True:
            query = get_all_categorized_transactions_query
        else:
            query = get_non_categorized_transactions_query    
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        self.close_connection()
        if (results):
            transactions_number = len(results)
            logger.info(f"Queried {transactions_number} transactions.")
            return results
        else:
            return []
        
    def update_transactions_categories_from_df(self, dataframe):
        logger = Logger.get_logger(__name__)
        cursor = self.mysql_connection.cursor()
        updated_ids = []
        for index, row in dataframe.iterrows():
            transaction_id = row['transaction_id']
            bank_category_id = row['category_id']
            update_transaction_category_query = ("UPDATE {} SET bank_category_id = %s, updated_at = CURRENT_TIMESTAMP() WHERE id = %s".format(self.table))
            update_transaction_category_parameters = (bank_category_id, transaction_id)
            cursor.execute(update_transaction_category_query, update_transaction_category_parameters)
            updated_ids.append(transaction_id)
        self.commit()
        self.close_connection()
        logger.info(f"Updated {len(updated_ids)} bank transactions with IDs: {updated_ids}")