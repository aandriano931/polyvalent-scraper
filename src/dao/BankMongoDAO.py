import os
from src.dao.MongoDAO import MongoDAO
import logging
import pymongo  
import datetime
import pytz

class BankMongoDAO(MongoDAO):
    
    def __init__(self, collection_name):
        mongo_database = os.getenv("MONGO_BANK_DATABASE")
        super().__init__(collection_name, mongo_database)
        # Create a compound index with unique constraint on relevant fields
        index_keys = [("data.amount", pymongo.ASCENDING), ("data.label", pymongo.ASCENDING), ("data.operation_date", pymongo.ASCENDING)]
        self.collection.create_index(index_keys, unique=True)
    
    def insert_one(self, dto_object):
        paris_timezone = pytz.timezone('Europe/Paris')
        current_time = datetime.now(paris_timezone).strftime("%Y-%m-%dT%H:%M:%SZ")
        document = {
                "data": {
                    "amount": dto_object.amount,
                    "label": dto_object.label,
                    "operation_date": dto_object.operation_date.strftime("%Y-%m-%d"),
                    "transaction_type": dto_object.transaction_type,
                    "value_date": dto_object.value_date.strftime("%Y-%m-%d"),
                },
                "created_at": current_time,
            }
        result = self.collection.insert_one(document)
        inserted_id = result.inserted_id
        logging.info(f"Inserted one bank document with ID: {inserted_id}")
        return result.inserted_id
    
    def insert_many(self, dto_collection):
        paris_timezone = pytz.timezone('Europe/Paris')
        current_time = datetime.now(paris_timezone).strftime("%Y-%m-%dT%H:%M:%SZ")
        documents = []
        for dto_object in dto_collection:
            document = {
                "data": {
                    "amount": dto_object.amount,
                    "label": dto_object.label,
                    "operation_date": dto_object.operation_date.strftime("%Y-%m-%d"),
                    "transaction_type": dto_object.transaction_type,
                    "value_date": dto_object.value_date.strftime("%Y-%m-%d"),
                },
                "created_at": current_time,
            }
            documents.append(document)
        result = self.collection.insert_many(documents)
        inserted_ids = result.inserted_ids
        logging.info(f"Inserted {len(inserted_ids)} bank documents with IDs: {inserted_ids}")
        return inserted_ids