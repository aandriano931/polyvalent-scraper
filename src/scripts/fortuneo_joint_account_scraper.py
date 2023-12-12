from src.data_processor.FortuneoDailyDataProcessor import FortuneoDailyDataProcessor

def main():
    # Process the joint account
    FortuneoDailyDataProcessor.process_bank_data("joint_account")
    
if __name__ == "__main__":
    main()