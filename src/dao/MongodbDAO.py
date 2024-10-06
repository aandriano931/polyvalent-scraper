import os
import time
from pymongo import MongoClient, errors
from src.tool.Logger import Logger

class MongodbDAO:
    
    logger = None
    
    def __init__(self):
        config = {
            "host": "mongodb",
            "user": os.getenv("MONGODB_USER"),
            "password": os.getenv("MONGODB_PASSWORD"),
            "database": 'car_hub',
            "authSource": 'admin'
        }
        self.mongodb_connection = self.connect_to_mongodb(config)

    def connect_to_mongodb(self, config, attempts=3, delay=2):
        logger = Logger.get_logger(__name__)
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                client = MongoClient(
                    host=config["host"],
                    username=config["user"],
                    password=config["password"],
                    authSource=config["authSource"]
                )
                # Check the connection
                client.admin.command('ping')
                return client[config["database"]]
            except (errors.ConnectionFailure, IOError) as err:
                if attempt == attempts:
                    # Attempts to reconnect failed; returning None
                    logger.error("Failed to connect, exiting without a connection: %s", err)
                    return None
                logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None

    def commit(self):
        # MongoDB does not require a commit operation like MySQL
        pass
        
    def close_connection(self):
        if self.mongodb_connection:
            self.mongodb_connection.client.close()