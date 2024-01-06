import os
import pandas as pd
from src.dao.BankTransactionDAO import BankTransactionDAO
from src.llm.BankCategoryGuesser import BankCategoryGuesser
from src.tool.Mailer import Mailer
from src.tool.Logger import Logger

COLUMNS = ['id', 'operation_date', 'label', 'debit', 'credit', 'category_id', 'category']

def get_transactions_df(categorized):
    bank_transaction_dao = BankTransactionDAO('ftn_joint_account')
    results = bank_transaction_dao.get_all(categorized)
    transactions = [dict(zip(COLUMNS, result)) for result in results]
    return pd.DataFrame(transactions)

def update_transactions_categories(dataframe):
    bank_transaction_dao = BankTransactionDAO('ftn_joint_account')
    bank_transaction_dao.update_transactions_categories_from_df(dataframe)   
    
def send_notification(dataframe_array):
    if os.getenv("ENABLE_MAIL") == "true":
        mailer = Mailer()
        subject = "New category assignements"
        message = "Categories were newly assigned to bank transactions. Information is provided in the tables below"
        mailer.send_notification_email_with_dataframe(subject, message, dataframe_array)
    else:
        logger = Logger.get_logger(__name__)
        logger.info('Successfully updated these transactions with guessed categories from BERT LLM')
        logger.info('\t'+ dataframe_array[0].to_string().replace('\n', '\n\t'))
        logger.warning('Failed to update these transactions')
        logger.warning('\t'+ dataframe_array[1].to_string().replace('\n', '\n\t'))

def main():
    # get training and guessing data and apply BERT embedding to it
    df_training_transactions = get_transactions_df(True)
    df_guessing_transactions = get_transactions_df(False)
    if df_guessing_transactions.empty:
        logger = Logger.get_logger(__name__)
        logger.info('There is 0 transaction without a category.')
    else:   
        # prepare data for LLM guessing
        category_guesser = BankCategoryGuesser()
        training_embedding = category_guesser.apply_bert_embedding(df_training_transactions)
        guessing_embedding = category_guesser.apply_bert_embedding(df_guessing_transactions)
        
        # Return the indexes of the most similar word embedding between training and guessing data and their similarity scores
        similarity_index, similarity_scores = category_guesser.get_similarity_index_and_scores(guessing_embedding, training_embedding)
            
        # dataframe for most similar transactions in test dataframe / unreliable results have been removed
        indices_to_keep_from_guessing_data = similarity_index.index.tolist()
        df_matching_guessing_transactions = df_guessing_transactions.iloc[indices_to_keep_from_guessing_data, :].reset_index(drop = True)

        # Find the indices of non-matching transactions
        indices_not_matched = df_guessing_transactions.index.difference(indices_to_keep_from_guessing_data)
        df_non_matching_guessing_transactions = df_guessing_transactions.iloc[indices_not_matched, :].reset_index(drop = True)
              
        # dataframe for most similar embedding/transactions in training dataframe
        df_matching_training_transactions = df_training_transactions.iloc[similarity_index, :].reset_index(drop = True)

        # update transactions categories
        df_update_categories = pd.DataFrame({
            'transaction_id': df_matching_guessing_transactions['id'],
            'category_id': df_matching_training_transactions['category_id'],
        })
        update_transactions_categories(df_update_categories)
        
        # generate summary dataframes and log or send them by email
        df_success_summary = pd.DataFrame({
            'Guessing Transaction ID': df_matching_guessing_transactions['id'],
            'Guessing Transaction label': df_matching_guessing_transactions['label'],
            'Assigned category': df_matching_training_transactions['category'],
            'Matching score' : similarity_scores,
        })
        
        df_fail_summary = pd.DataFrame({
            'Failed Guessing Transaction ID': df_non_matching_guessing_transactions['id'],
            'Failed Guessing Transaction label': df_non_matching_guessing_transactions['label'],
        })
        
        array_dataframes = []
        if not df_success_summary.empty:       
            array_dataframes.append(df_success_summary)
        if not df_fail_summary.empty:       
            array_dataframes.append(df_fail_summary)

        send_notification([df_success_summary, df_fail_summary])   
        
if __name__ == "__main__":
    main()