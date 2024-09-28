import csv
import os, sys
from src.dao.BankTransactionDAO import BankTransactionDAO
from datetime import datetime
from src.dto.BankTransactionDTO import BankTransactionDTO

def transform_csv_to_dto(csv_file_path):
    transactions = []

    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if reader.line_num == 1:
                continue
                    
            operation_date = datetime.strptime(row['Date operation'], '%d/%m/%Y').date()
            value_date = datetime.strptime(row['Date valeur'], '%d/%m/%Y').date()
            label = row['libelle']
            debit = float(row['Debit'].replace(',', '.')) if row['Debit'] else None
            credit = float(row['Credit'].replace(',', '.')) if row['Credit'] else None
            amount = -debit if debit else credit
            transaction_type = "debit" if debit else "credit"
            ftn_dto = BankTransactionDTO(
                amount=amount,
                label=label,
                operation_date=operation_date,
                transaction_type=transaction_type,
                value_date=value_date
            )
            transactions.append(ftn_dto)

    return transactions

def main():
    ftn_history_file_path = os.getenv("FT_PERSONAL_HISTORY_FILE_PATH")
    transactions = transform_csv_to_dto(ftn_history_file_path)
    transactions.sort(key=lambda x: x.operation_date)
    ftn_dao = BankTransactionDAO('ftn_personal_account') 
    ftn_dao.insert_many(transactions)
    
if __name__ == "__main__":
    main()