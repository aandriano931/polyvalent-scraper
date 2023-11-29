from dao.MysqlDAO import MysqlDAO

class BankAccountDAO(MysqlDAO):
    
    def __init__(self):
        self.table = 'bank_account'
        super().__init__()
        
    def get_one_by_alias(self, bank_account_alias):
        cursor = self.mysql_connection.cursor()
        get_account_by_alias_query = ("SELECT id FROM {} WHERE alias = %s LIMIT 1".format(self.table))
        get_account_by_alias_parameters = (bank_account_alias,)
        cursor.execute(get_account_by_alias_query, get_account_by_alias_parameters)
        result = cursor.fetchone()
        cursor.close()
        self.close_connection()
        if (result):
            self.logger.info(f"Queried bank account with ID: {result[0]}")
            return result[0]
        else:
            return None