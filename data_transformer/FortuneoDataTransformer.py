from datetime import datetime
from dto.BankTransactionDTO import BankTransactionDTO

class FortuneoDataTransformer:

    def transform_collection(self, raw_data_collection):
        transformed_data_list = []
        for raw_data in raw_data_collection:
            operation_date_str = raw_data[1]
            value_date_str = raw_data[2]
            label = raw_data[3]
            if raw_data[4]:
                amount_str = raw_data[4]
            else:
                amount_str = raw_data[5]
            operation_date = datetime.strptime(operation_date_str, '%d/%m/%Y').date()
            value_date = datetime.strptime(value_date_str, '%d/%m/%Y').date()
            amount = float(amount_str)
            transaction_type = "debit" if amount < 0 else "credit"
            amount = abs(amount)
            transformed_data = BankTransactionDTO(
                amount=amount,
                label=label,
                operation_date=operation_date,
                transaction_type=transaction_type,
                value_date=value_date
            )
            transformed_data_list.append(transformed_data)
        return transformed_data_list