from dao.MysqlDAO import MysqlDAO
import uuid

class BankMysqlDAO(MysqlDAO):
    
    def __init__(self, mysql_database):
        super(BankMysqlDAO, self).__init__(mysql_database)
    
    def insert_one(self, dto_object):
        cursor = self.mysql_connection.cursor()
        add_transaction_query = ("INSERT INTO Transaction "
               "(transaction_id, credit, debit, label, operation_date, value_date) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        
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
        add_transaction_parameters = (new_uuid, credit, debit, label, operation_date, value_date)
        cursor.execute(add_transaction_query, add_transaction_parameters)
        inserted_id = str(new_uuid)
        self.mysql_connection.commit()
        cursor.close()
        self.mysql_connection.close()
        self.logger.info(f"Inserted one bank document with ID: {inserted_id}")
        return inserted_id
    
    def insert_many(self, dto_collection):
        cursor = self.mysql_connection.cursor()
        inserted_ids = []
        for dto_object in dto_collection:
            add_transaction_query = ("INSERT INTO Transaction "
               "(transaction_id, credit, debit, label, operation_date, value_date) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
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
            add_transaction_parameters = (new_uuid, credit, debit, label, operation_date, value_date)
            cursor.execute(add_transaction_query, add_transaction_parameters)
            inserted_ids.append(new_uuid)
        self.mysql_connection.commit()
        cursor.close()
        self.mysql_connection.close()
        self.logger.info(f"Inserted {len(inserted_ids)} bank documents with IDs: {inserted_ids}")
        return inserted_ids