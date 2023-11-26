from tool.LoggingToolBox import LoggingToolBox
from data_processor.FortuneoDailyDataProcessor import FortuneoDailyDataProcessor

LoggingToolBox.set_logger()
# Process the personal account
FortuneoDailyDataProcessor.process_bank_data("personal_account")