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
    length = len(df)
    non_string_rows = df[~df[column_name].apply(lambda x: isinstance(x, str))]

    if verbose:
        na_len = len(non_string_rows)
        prc = '{0:.2f}'.format(100*na_len/length)
        print("{} rows found with non string elements for column {} ({}%)".format(na_len,column_name,prc))
        
    df_removed = df.drop(non_string_rows.index)

    return df_removed


def process_df(df:pd.DataFrame, text_column:str, target_column:str, verbose=True) -> pd.DataFrame:
    """Takes a pandas dataframe and returns a new one with no NA values and without useless instances
    
    Arguments

        df: pd.DataFrame
            dataframe containing text to analyse

        text_column: str
            text column name (from df) with text content
        
        target_column: str
            target column name (from df) with value to predict
        
        verbose: bool
            whether to print the amount of problematic rows found
    
    Returns
    
        new_df: pd.DataFrame
            processed dataframe
    
    """
    length = len(df)
    new_df = delete_non_string_rows(df,text_column,verbose)
    new_df = new_df[new_df[text_column].notna()]  # not actually needed
    new_df = new_df[new_df['sel'].notna()]

    if verbose:
        freq_7 = len(new_df[new_df['max_num'] > 6])
        prc_7 = '{0:.2f}'.format(100*freq_7/length)
        print("Deleting {} columns for which max target value is over 7 ({}%)".format(freq_7,prc_7))

    new_df = new_df.drop(new_df[new_df['max_num'] > 6].index)

    if verbose:
        print("{} available rows after processing".format(len(new_df)))

    return new_df


def procesar_adela(df):
    # procesamiento especial para caso Adela
    df.loc[df['opt_left']=='Producir el alimento contra  déficit vitamínico','opt_left'] = 'Producir el alimento contra déficit vitamínico'
    df.loc[df['opt_left']=='Preservar el recurso natural escaso.','opt_left'] = 'Preservar el recurso natural escaso'
    df.loc[df['opt_left']=='Producir el alimento contra déficit vitamínico.','opt_left'] = 'Producir el alimento contra déficit vitamínico'
    df.loc[df['opt_left']=='Producir el alimento contra el déficit vitamínico.','opt_left'] = 'Producir el alimento contra déficit vitamínico'

    df.loc[df['opt_right']=='Resguardar las tradiciones identitarias.','opt_right'] = 'Resguardar las tradiciones identitarias'
    df.loc[df['opt_right']=='Beneficiar la salud de niños y ancianos.','opt_right'] = 'Beneficiar la salud de niños y ancianos'
    
    df = df[df['opt_left'] != 'El caso parece muy irreal']
    df = df[df['opt_left'] != 'adios']
    df = df[df['opt_left'] != 'Tangananica']

    return df


class StemmerTokenizer:
    def __init__(self,stem=True,rmv_punctuation=False):
        self.stem = stem
        self.rmv_words = stop_words + [',','.',':',';','...','(',')'] if rmv_punctuation else stop_words
        self.ps = SnowballStemmer('spanish')
    
    def __call__(self, doc):
        doc_tok = word_tokenize(doc)
        doc_tok = [t for t in doc_tok if t not in self.rmv_words]
        doc_tok = [self.ps.stem(t) for t in doc_tok] if self.stem else doc_tok
        return doc_tok


def make_BoW_preprocess(tokenizer:StemmerTokenizer,column:str,max_ngram:int=2,min_ngram:int=1,mindf=1,maxdf=1.0) -> ColumnTransformer:
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
        
        mindf: int/float, default 1
            minimum number/proportion of appearances for an n_gram to be considered

        maxdf: int/float, default 1.0
            maximum number/proportion of appearances for an n_gram to be considered
    
    Returns
    
        preprocessing: ColumnTransformer
            ColumnTransformer that should be put in a scikit-learn pipeline

    """
    
    bog = CountVectorizer(
        tokenizer = tokenizer,
        ngram_range=(min_ngram,max_ngram),
        min_df = mindf,
        max_df = maxdf,
        )

    preprocessing = ColumnTransformer(
        transformers=[('bag-of-words',bog,column)]
    )

    return preprocessing
