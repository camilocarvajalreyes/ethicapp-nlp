import yaml
import pandas as pd
import os


# Merge dictionaries - source: ChatGPT
def merge_dictionaries(list_of_dictionaries):
    merged_dict = {}
    
    for dictionary in list_of_dictionaries:
        merged_dict.update(dictionary)
    
    return merged_dict


with open('datamap.yaml', 'r') as stream:
    datamap = yaml.safe_load(stream)
    for k in datamap.keys():
        if '_fases' in k:
            datamap[k] = merge_dictionaries(datamap[k])
    for k in datamap.keys():
        if '_fases' in k:
            for kk in datamap[k].keys():
                datamap[k][kk] = merge_dictionaries(datamap[k][kk])


def files_in_folder(folder):
    return [file for file in os.listdir(folder) if '.csv' in file]


def iteraciones_datamap(nombre):
    if '_fases' in nombre:
        raise KeyError("La variable nombre deben ser alguna entre 'adela', 'alicia', 'julieta' y 'laura'")
    try:
        iteraciones = datamap[nombre]
    except KeyError:
         raise KeyError("La variable nombre deben ser alguna entre 'adela', 'alicia', 'julieta' y 'laura'")
    return iteraciones


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
    iteraciones = iteraciones_datamap(nombre)
    dfs = []
    for curso in iteraciones:
            folder = datamap['parent']+curso+'/'
            files = files_in_folder(folder)
            for file in  files:
                df = pd.read_csv(folder + file, delimiter=';',index_col='id')
                df['curso'] = curso
                dfs.append(df)
    df = pd.concat(dfs)
    df = df.drop(columns=['name','rut'])

    return df


def fase(df:pd.DataFrame,fase:int,caso:str) -> pd.DataFrame:
    """
     Filtra un dataframe...
    """
    condition_tuples = []
    key_caso = caso + '_fases'

    for curso in datamap[key_caso].keys():
        for indice in datamap[key_caso][curso][fase]:
            condition_tuples.append((curso,indice))
    
    return df[(df['phase'],df['curso']) in condition_tuples]
