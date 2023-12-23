import os
import mysql.connector
import time
from src.tool.Logger import Logger

class MysqlDAO:
    
    logger = None
    
    def __init__(self):
        config = {
            "host": "mysql",
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": 'home-hub',
        }
        self.mysql_connection = self.connect_to_mysql(config)

    def connect_to_mysql(self, config, attempts=3, delay=2):
        logger = Logger.get_logger()
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**config)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
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
        self.mysql_connection.commit()
        
    def close_connection(self):
        self.mysql_connection.close()