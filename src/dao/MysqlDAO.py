import os
import mysql.connector
import logging
import time

class MysqlDAO:
    
    logger = None
    
    def __init__(self):
        if not self.__class__.logger:
            self.set_logger()
        config = {
            "host": "mysql",
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": 'home-hub',
        }
        self.mysql_connection = self.connect_to_mysql(config)

    def set_logger(self):
        if not self.__class__.logger:
            self.__class__.logger = logging.getLogger(__name__)
            self.__class__.logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            # Log to console
            handler_added = any(isinstance(g, logging.StreamHandler) for g in self.__class__.logger.handlers)
            if not handler_added:
                handler = logging.StreamHandler()
                handler.setFormatter(formatter)
                self.__class__.logger.addHandler(handler)

            # Also log to a file
            file_handler_added = any(isinstance(h, logging.FileHandler) for h in self.__class__.logger.handlers)
            if not file_handler_added:
                file_handler = logging.FileHandler("cpy-errors.log")
                file_handler.setFormatter(formatter)
                self.__class__.logger.addHandler(file_handler) 
    
    def connect_to_mysql(self, config, attempts=3, delay=2):
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**config)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    self.__class__.logger.info("Failed to connect, exiting without a connection: %s", err)
                    return None
                self.__class__.logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None
    
    def close_connection(self):
        self.mysql_connection.close()