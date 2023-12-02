from data_processor.FortuneoDailyDataProcessor import FortuneoDailyDataProcessor

def main():
    # Process the personal account
    FortuneoDailyDataProcessor.process_bank_data("personal_account")
    
if __name__ == "__main__":
    main()