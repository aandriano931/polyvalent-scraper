import logging
import os
import pytz
from datetime import datetime
from pymongo import MongoClient

class MongoDAO:
    
    def __init__(self, collection_name, mongo_database=None):
        mongo_username = os.getenv("MONGO_USERNAME")
        mongo_password = os.getenv("MONGO_PASSWORD") 
        mongo_port = os.getenv("MONGO_PORT")
        self.client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@mongo:{mongo_port}/")
        self.db = self.client[mongo_database]
        self.collection = self.db[collection_name]

    def close_connection(self):
        self.client.close()