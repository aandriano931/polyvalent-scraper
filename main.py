import os
import sys
from src.scripts import fortuneo_joint_account_history_extraction, fortuneo_joint_account_scraper, fortuneo_personal_account_scraper
from src.tool.Mailer import Mailer
from src.tool.Logger import Logger

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <action>")
        sys.exit(1)
    action = sys.argv[1]
    
    try:
        if action == "ftn_joint_scrape":
            fortuneo_joint_account_scraper.main()
        elif action == "ftn_joint_history":
            fortuneo_joint_account_history_extraction.main()
        elif action == "ftn_perso_scrape":
            fortuneo_personal_account_scraper.main()
        else:
            print("Invalid action. Supported actions: extract_website, insert_website, extract_csv, insert_csv")
    except Exception as e:
        error_message = f"An error occurred during scraping: {str(e)}"
        send_error_notification(error_message)         

def send_error_notification(error_message):
    if os.getenv("LOG_PATH") == "true":
        mailer = Mailer()
        subject = "Error Notification"
        mailer.send_notification_email(subject, error_message)
    else:
        logger = Logger.get_logger()
        logger.error('%s', error_message)    

if __name__ == "__main__":
    main()
