import logging
import os

class LoggingToolBox:
    
    @staticmethod
    def set_logger():
        log_level = os.getenv("PYTHON_LOG_LEVEL", "INFO")
        numeric_level = getattr(logging, log_level, None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {log_level}")
        logging.basicConfig(level=numeric_level)