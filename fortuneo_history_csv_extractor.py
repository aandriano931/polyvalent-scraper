import csv
import logging
import sys
from dao.BankDAO import BankDAO
from datetime import datetime
from dto.BankTransactionDTO import BankTransactionDTO
from tool.LoggingToolBox import LoggingToolBox

def transform_csv_to_dto(csv_file_path):
    transactions = []

    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if reader.line_num == 1:
                continue

            operation_date = datetime.strptime(row['Date opération'], '%d/%m/%Y').date()
            value_date = datetime.strptime(row['Date valeur'], '%d/%m/%Y').date()
            label = row['libellé']
            debit = float(row['Débit'].replace(',', '.')) if row['Débit'] else None
            credit = float(row['Crédit'].replace(',', '.')) if row['Crédit'] else None
            amount = -debit if debit else credit
            transaction_type = "debit" if debit else "credit"
            fortuneo_dto = BankTransactionDTO(
                amount=amount,
                label=label,
                operation_date=operation_date,
                transaction_type=transaction_type,
                value_date=value_date
            )
            transactions.append(fortuneo_dto)

    return transactions

LoggingToolBox.set_logger()

fortuneo_history_file_path = './data_source/file/full_historique_compte_joint.csv'
transactions = transform_csv_to_dto(fortuneo_history_file_path)
transactions.sort(key=lambda x: x.operation_date)

fortuneo_dao = BankDAO('fortuneo_joint_account_data'); 
fortuneo_dao.insert_many(transactions)