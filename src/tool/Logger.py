import os
import logging

class Logger:
   
    @staticmethod   
    def get_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            # Log to console
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            # Also log to a file
            file_handler = logging.FileHandler(os.getenv("LOG_PATH"))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
                
        return logger 