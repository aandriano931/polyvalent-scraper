import sys
from src.scripts import fortuneo_joint_account_history_extraction, fortuneo_joint_account_scraper, fortuneo_personal_account_scraper

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <action>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "ftn_joint_scrape":
        fortuneo_joint_account_scraper.main()
    elif action == "ftn_joint_history":
        fortuneo_joint_account_history_extraction.main()
    elif action == "ftn_perso_scrape":
        fortuneo_personal_account_scraper.main()
    else:
        print("Invalid action. Supported actions: extract_website, insert_website, extract_csv, insert_csv")

if __name__ == "__main__":
    main()
