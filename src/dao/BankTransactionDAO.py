from src.dao.MysqlDAO import MysqlDAO
from src.dao.BankAccountDAO import BankAccountDAO
import uuid

class BankTransactionDAO(MysqlDAO):
    
    def __init__(self, bank_account_alias):
        self.table = 'bank_transaction'
        self.bank_account_alias = bank_account_alias
        super().__init__()
    
    def insert_one(self, dto_object):
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
        self.mysql_connection.commit()
        cursor.close()
        self.close_connection()
        self.__class__.logger.info(f"Inserted one bank transaction with ID: {inserted_id}")
        return inserted_id
    
    def insert_many(self, dto_collection):
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
        self.mysql_connection.commit()
        cursor.close()
        self.close_connection()
        self.__class__.logger.info(f"Inserted {len(inserted_ids)} bank transactions with IDs: {inserted_ids}")
        return inserted_ids