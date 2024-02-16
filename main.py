import os
import sys
from src.data_processor.FtnDataProcessor import FtnDataProcessor
from src.scripts import category_automatic_guess, ftn_joint_account_history_extraction
from src.tool.Mailer import Mailer
from src.tool.Logger import Logger
from src.exceptions.NoTransactionException import NoTransactionException

def main():
    if len(sys.argv) > 3:
        print("Usage: python main.py <action> [date_delta]")
        sys.exit(1)
    action = sys.argv[1]
    date_delta = int(sys.argv[2]) if len(sys.argv) == 3 else 1
    
    try:
        if action == "ftn_joint_scrape":
            FtnDataProcessor.process_bank_data("joint_account", date_delta)
        elif action == "ftn_joint_history":
            ftn_joint_account_history_extraction.main()
        elif action == "ftn_perso_scrape":
            FtnDataProcessor.process_bank_data("personal_account", date_delta)
        elif action == "guess_category":
            category_automatic_guess.main()  
        else:
            print("Invalid action. Supported actions: ftn_joint_scrape, ftn_perso_scrape, ftn_joint_history, guess_category")
    except NoTransactionException as e:
        send_info_notification(str(e))
    except ValueError as e:
        error_message = f"An error occurred during automatic scraping: {str(e)}"
        send_error_notification(error_message)         

def send_error_notification(error_message):
    if os.getenv("ENABLE_MAIL") == "true":
        mailer = Mailer()
        subject = "Error Notification (Polyvalent Scraper)"
        mailer.send_notification_email(subject, error_message)
    else:
        logger = Logger.get_logger(__name__)
        logger.error('%s', error_message)
        
def send_info_notification(info_message):
    if os.getenv("ENABLE_MAIL") == "true":
        mailer = Mailer()
        subject = "Information Notification (Polyvalent Scraper)"
        mailer.send_notification_email(subject, info_message)
    else:
        logger = Logger.get_logger(__name__)
        logger.info('%s', info_message)    
    

if __name__ == "__main__":
    main()
