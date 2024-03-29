"""Some text basic exploration functions"""
import pandas as pd
import numpy as np
from collections import Counter
from nltk import ngrams
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from IPython.display import Markdown, display


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
    list_words = ' '.join(df[column]).lower().split()
    list_words = [w for w in list_words if w not in ignore]

    if n_grams == 1:
        tokens =  pd.Series(list_words).value_counts()
        tokens = tokens.drop(ignore,errors='ignore')
        tokens = tokens[:limit]
    else:
        ngram_counts = Counter(ngrams(list_words, n_grams))
        comunes_2g = ngram_counts.most_common(limit)
        tokens = pd.Series([tup[1] for tup in comunes_2g],index=[' '.join(tup[0]) for tup in comunes_2g])
    
    return tokens


def plot_token_frequency(tokens:pd.Series,title=None,fig_size=(5,4),ax=None):
    """
    Takes a Pandas Series of value counts (of tokens sorted by frequency) and plots it
    """
    title = 'Tokens' if title is None else title
    tokens.plot.barh(figsize=fig_size,title=title,ax=ax)


def wordcloud_from_column(df:pd.DataFrame,column:str,maxfont:int=40,ignore:list=[]):
    """
    It generates a wordcloud visualisation from the dataframe column (values must be strings)
    source: https://amueller.github.io/word_cloud/auto_examples/simple.html

    Arguments

        df: pd.DataFrame
            dataframe containing text to analyse

        column: str
            target column name (from df) with text content
        
        maxfont: int, default 40
            maximum font to use in visualisation, if set to None it will be generated from frequencies
        
        ignore: list, default []
            list of words to ignore
    
    """
    # to do example coloured by group: https://amueller.github.io/word_cloud/auto_examples/colored_by_group.html

    text = ' '.join(df[column]).lower()
    
    for word in ignore:
        text = text.replace(' '+ word + ' ',' ')
    # tokens =  pd.Series(' '.join(df[column]).lower().split())

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    wordcloud = WordCloud(max_font_size=maxfont).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def comment_length(df:pd.DataFrame,column:str,ignore:list=[]) -> np.array:
    """
    DESCRIPTION

    Arguments

        df: pd.DataFrame
            dataframe containing text to analyse

        column: str
            target column name (from df) with text content
        
        ignore: list, default []
            list of words to ignore
    
    """
    list_words = df[column].apply(lambda text: text.lower().split())
    list_words = list_words.apply(lambda list_text: [w for w in list_text if w not in ignore])
    return list_words.apply(lambda list_text: len(list_text)).to_numpy()


def basic_stats(arr):
    dic = {'mean':np.mean(arr),'median':np.median(arr),'std':np.std(arr),
        'min':np.min(arr),'max':np.max(arr)}
    return dic


def print_basic_stats(arr):
    dic = basic_stats(arr)
    print("Media:", dic['mean'])
    print("Desviación estándar:", dic['std'])
    print("Mediana:", dic['median'])
    print("Mínimo:", dic['min'])
    print("Máximo:", dic['max'])


def print_table_md(headers, data):
    table_md = '| ' + ' | '.join(headers) + ' |\n'
    table_md += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'

    for row in data:
        table_md += '| ' + ' | '.join(str(item) for item in row) + ' |\n'

    display(Markdown(table_md))
