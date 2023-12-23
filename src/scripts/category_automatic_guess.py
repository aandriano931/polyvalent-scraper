import pandas as pd
from src.dao.BankTransactionDAO import BankTransactionDAO
from src.llm.BankCategoryGuesser import BankCategoryGuesser

COLUMNS = ['id', 'operation_date', 'label', 'debit', 'credit', 'category_id', 'category']

def get_transactions_df(categorized):
    bank_dao = BankTransactionDAO('fortuneo_joint_account')
    results = bank_dao.get_all(categorized)
    transactions = [dict(zip(COLUMNS, result)) for result in results]
    return pd.DataFrame(transactions)

def main():

    # get training and guessing data and apply BERT embedding to it
    df_training_transactions = get_transactions_df(True)
    df_guessing_transactions = get_transactions_df(False)
    
    # prepare data for LLM guessing
    category_guesser = BankCategoryGuesser()
    training_embedding = category_guesser.apply_bert_embedding(df_training_transactions)
    guessing_embedding = category_guesser.apply_bert_embedding(df_guessing_transactions)
    
    # Return the indexes of the most similar word embedding between training and guessing data and their similarity scores
    similarity_index, similarity_scores = category_guesser.get_similarity_index_and_scores(guessing_embedding, training_embedding)
        
    # dataframe for most similar transactions in test dataframe / unreliable results have been removed
    indices_to_keep_from_test_data = similarity_index.index.tolist()
    df_matching_test_transactions = df_guessing_transactions.iloc[indices_to_keep_from_test_data, :].reset_index(drop = True)

    # dataframe for most similar embedding/transactions in training dataframe
    df_matching_training_transactions = df_training_transactions.iloc[similarity_index, :].reset_index(drop = True)

    # return final comparaison dataframe
    result_df = pd.DataFrame({
        'Test Transaction label': df_matching_test_transactions['label'],
        'Most Similar Training Entry': df_matching_training_transactions['label'],
        'Scores': similarity_scores,
        'Matched category name': df_matching_training_transactions['category'],
    })
    result_df.sort_values(by='Scores', ascending=False, inplace=True)
    
    print(result_df)
    
    
if __name__ == "__main__":
    main()