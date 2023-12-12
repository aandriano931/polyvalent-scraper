class BankTransactionDTO:
    def __init__(self, amount, label, operation_date, transaction_type, value_date):
        self.amount = amount
        self.label = label
        self.operation_date = operation_date
        self.transaction_type = transaction_type
        self.value_date = value_date