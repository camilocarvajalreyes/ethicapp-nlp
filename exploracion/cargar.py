import yaml
import pandas as pd
import os


# Read YAML file - source: ChatGPT
with open('datamap.yaml', 'r') as stream:
    datamap = yaml.safe_load(stream)


def files_in_folder(folder):
    return [file for file in os.listdir(folder) if '.csv' in file]


def df_caso(nombre:str) -> pd.DataFrame:
    """
    Retorna un dataframe de pandas con todos los contenidos del caso en cuestión

    Argumentos
    
        nombre: str
            nombre del caso, uno entre: 'adela', 'alicia', 'julieta' y 'laura'
        
    Retorna

        df: pd.DataFrame
            un dataframe de pandas con las respuestas de todos los cursos y secciones
    """
    try:
        iteraciones = datamap[nombre]
    except KeyError:
         raise KeyError("La variable nombre deben ser alguna entre 'adela', 'alicia', 'julieta' y 'laura'")
    dfs = []
    for curso in iteraciones:
            folder = datamap['parent']+curso+'/'
            files = files_in_folder(folder)
            dfs += [pd.read_csv(folder + file, delimiter=';',index_col='id') for file in files]
    df = pd.concat(dfs)
    df = df.drop(columns=['name','rut'])

    return df
