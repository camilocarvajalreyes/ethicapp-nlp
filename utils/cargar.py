import yaml
import pandas as pd
import os


# Merge dictionaries - source: ChatGPT
def merge_dictionaries(list_of_dictionaries):
    merged_dict = {}
    
    for dictionary in list_of_dictionaries:
        merged_dict.update(dictionary)
    
    return merged_dict


def read_datamap(file):
    with open(file, 'r') as stream:
        datamap = yaml.safe_load(stream)
        for k in datamap.keys():
            if '_fases' in k:
                datamap[k] = merge_dictionaries(datamap[k])
        for k in datamap.keys():
            if '_fases' in k:
                for kk in datamap[k].keys():
                    datamap[k][kk] = merge_dictionaries(datamap[k][kk])
    return datamap

try:
    datamap = read_datamap('datamap.yaml')
except FileNotFoundError:
    datamap = read_datamap('../datamap.yaml')


def files_in_folder(folder):
    try:
        files = [file for file in os.listdir(folder) if '.csv' in file]
    except FileNotFoundError:
        files = []
    return files


def iteraciones_datamap(nombre):
    if '_fases' in nombre:
        raise KeyError("La variable nombre deben ser alguna entre 'adela', 'alicia', 'julieta' y 'laura'")
    try:
        iteraciones = datamap[nombre]
    except KeyError:
         raise KeyError("La variable nombre deben ser alguna entre 'adela', 'alicia', 'julieta' y 'laura'")
    return iteraciones


def df_caso(nombre:str,chat=False,seccion=False,verbose=False) -> pd.DataFrame:
    """
    Retorna un dataframe de pandas con todos los contenidos del caso en cuestión

    Argumentos
    
        nombre: str
            nombre del caso, uno entre: 'adela', 'alicia', 'julieta' y 'laura'

        chat: bool, default = False
            If True retorna un dataframe con los chats disponibles para el caso

        seccion: bool, default = False
            If True el dataframe contiene una columna con la seccion
        verbose: bool, default = False
            If True imprime las secciones encontradas
        
    Retorna

        df: pd.DataFrame
            un dataframe de pandas con las respuestas de todos los cursos y secciones
    """
    iteraciones = iteraciones_datamap(nombre)
    dfs = []
    if verbose:
        print("Secciones encontradas:")
    for curso in iteraciones:
        if chat:
            folder = datamap['parent']+curso+'/chat/'
        else:
            folder = datamap['parent']+curso+'/'
        try:
            files = files_in_folder(folder)
            if files == []:
                raise FileNotFoundError
        except FileNotFoundError:
            folder = '../' + folder
            files = files_in_folder(folder)
        for file in  files:
            df = pd.read_csv(folder + file, delimiter=';',index_col='id')
            if verbose:
                print('\t',file)
            elms = file.split('.')
            seccion = int(elms[2])
            df['curso'] = curso
            df['seccion'] = seccion
            dfs.append(df)
    if verbose:
        print('\n')
    df = pd.concat(dfs)
    df = df.drop(columns=['name','rut'])

    return df


def fase(df:pd.DataFrame,fase:int,caso:str) -> pd.DataFrame:
    """
     Filtra un dataframe de modo que retorne las instancias de la fase en cuestión
    """
    condition_df = []
    key_caso = caso + '_fases'

    for curso in datamap[key_caso].keys():
        for indice in datamap[key_caso][curso][fase]:
            condition_df.append(df.loc[(df['phase'] == indice) & (df['curso'] == curso)])
    
    return pd.concat(condition_df)


def columna_fase(df:pd.DataFrame,caso:str) -> pd.DataFrame:
    """Agrega la columna fase al DF. No optimizada"""
    new_df = df.copy()
    new_df['etapa'] = None
    for etapa in ['Ind1','Grup','Ind2']:
        df_caso = fase(df,etapa,caso)
        new_df.loc[new_df.index.isin(df_caso.index), 'etapa'] = etapa
    return new_df
