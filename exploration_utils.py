"""Some text basic exploration functions"""
import pandas as pd
from collections import Counter
from nltk import ngrams


def most_common(df:pd.DataFrame,column:str,n_grams:int=1,limit:int=10,ignore:list=[]) -> pd.Series:
    """
    Takes a df and a column (name of it, as a string), it returns a Pandas Series with n-grams with their respective frequency

    Arguments

        df: pd.DataFrame
            dataframe containing text to analyse

        column: str
            target column name (from df) with text content
        
        n_grams: int, default 1
            whether to  consider unigrams (1, i.e., single words), two grams, three grams, etc

        limit: int, default 10
            limits the number of most-common n_grams to return
        
        ignore: list, default []
            list of words to ignore

    Returns

        tokens: pd.Series
            pandas Series with n_gram to frequency for the given dataframe and column
    
    """
    if n_grams == 1:
        tokens =  pd.Series(' '.join(df[column]).lower().split()).value_counts()
        tokens = tokens.drop(ignore,errors='ignore')
        tokens = tokens[:limit]
    else:
        ngram_counts = Counter(ngrams(' '.join(df[column]).lower().split(), n_grams))
        comunes_2g = ngram_counts.most_common(limit)
        tokens = pd.Series([tup[1] for tup in comunes_2g],index=[' '.join(tup[0]) for tup in comunes_2g])
    
    return tokens


def plot_token_frequency(tokens:pd.Series,title=None,fig_size=(5,4)):
    """
    Takes a Pandas Series of value counts (of tokens sorted by frequency) and plots it
    """
    title = 'Tokens' if title is None else title
    tokens.plot.barh(figsize=fig_size,title=title)
