"""Text pre-processing utils"""
import pandas as pd
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer

stop_words = stopwords.words('spanish')


def delete_non_string_rows(df:pd.DataFrame, column_name:str, verbose=True) -> pd.DataFrame:
    """Takes a pandas dataframe and removes rows for which the element of a given column is not a string
    
    Arguments

        df: pd.DataFrame
            dataframe containing text to analyse

        column: str
            target column name (from df) with text content
        
        verbose: bool
            whether to print the amount of problematic rows found
    
    Returns
    
        df_removed: pd.DataFrame
            clean dataframe (without non string elements for the given column)
    """
    non_string_rows = df[~df[column_name].apply(lambda x: isinstance(x, str))]

    if verbose:
        print("{} rows found with non string elements for column {}".format(len(non_string_rows),column_name))
        
    df_removed = df.drop(non_string_rows.index)

    return df_removed


class StemmerTokenizer:
    def __init__(self):
        self.ps = SnowballStemmer('spanish')
    
    def __call__(self, doc):
        doc_tok = word_tokenize(doc)
        doc_tok = [t for t in doc_tok if t not in stop_words]
        return [self.ps.stem(t) for t in doc_tok]


def make_BoW_preprocess(tokenizer:StemmerTokenizer,column:str,max_ngram:int=2,min_ngram:int=1) -> ColumnTransformer:
    """
    Wraps up tokenising and n_gram selection into a ColumnTransformer for a dataframe

    Arguments

        tokenizer: StemmerTokenizer
            Instance of a custom class StemmerTokenizer, which reloves stop words and keeps the stem of words

        column: str
            target column name (from df) with text content
        
        max_ngram: int, default 2
            maximum n_gram to consider as features

        min_ngram: int, default 1
            minimum ngram to consider, 1 being single words
    
    Returns
    
        preprocessing: ColumnTransformer
            ColumnTransformer that should be put in a scikit-learn pipeline

    """
    
    bog = CountVectorizer(
        tokenizer = tokenizer,
        ngram_range=(min_ngram,max_ngram)
        )

    preprocessing = ColumnTransformer(
        transformers=[('bag-of-words',bog,column)]
    )

    return preprocessing
