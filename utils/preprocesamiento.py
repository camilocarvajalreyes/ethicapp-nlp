"""Text pre-processing utils"""
import pandas as pd


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
