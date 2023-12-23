import os
import numpy as np 
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class BankCategoryGuesser:

    HIGH_RELIABILITY_THRESHOLD = 0.90

    def __init__(self):
        nltk.download('punkt')
        model_path = "./data_source/bank_transactions_model"
        if not os.path.exists(model_path):
            self.model = SentenceTransformer('paraphrase-mpnet-base-v2')
            self.model.save(model_path)
        else:
            self.model = SentenceTransformer(model_path)

    def apply_bert_embedding(self, dataframe):
        bert_input = self.get_llm_cleaned_data_from_df(dataframe, 'label')
        embeddings = self.model.encode(bert_input, show_progress_bar = True)
        return np.array(embeddings)
    
    def get_llm_cleaned_data_from_df(self, dataframe, dataframe_column):
        raw_data = dataframe[dataframe_column]
        cleaned_data = raw_data.apply(lambda x: self.clean_text_for_llm(x))
        return cleaned_data.tolist()
    
    def clean_text_for_llm(self, raw_text):
        text = raw_text.lower()
        text = re.sub(r'[^\w\s]|https?://\S+|www\.\S+|https?:/\S+|[^\x00-\x7F]+|cesson sevigne|\d+', '', str(text).strip())
        text_list = word_tokenize(text)
        return ' '.join(text_list)
   
    def get_similarity_index_and_scores(self, guessing_embedding, training_embedding):
        # Find the most similar word embedding with unseen data in the training data
        similarity_new_data = cosine_similarity(guessing_embedding, training_embedding)
        similarity_df = pd.DataFrame(similarity_new_data)
        # Keep only the matches with score >= to a predetermined threshold
        high_probability_df = similarity_df[similarity_df.apply(lambda row: row.max(), axis=1) >= self.HIGH_RELIABILITY_THRESHOLD]
        similarity_index = high_probability_df.idxmax(axis = 1)
        scores = high_probability_df.max(axis = 1).reset_index(drop = True)
        return similarity_index, scores
    
    