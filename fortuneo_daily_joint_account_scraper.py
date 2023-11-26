from tool.LoggingToolBox import LoggingToolBox
from data_processor.FortuneoDailyDataProcessor import FortuneoDailyDataProcessor

LoggingToolBox.set_logger()
# Process the joint account
FortuneoDailyDataProcessor.process_bank_data("joint_account")