# Imports de pacotes de terceiros
import pandas as pd

def combinar_abas(df1: pd.DataFrame, df2: pd.DataFrame, left_chave, right_chave, join): 
    try:
        consolidado = pd.merge(df1, df2, left_on=left_chave, right_on=right_chave, how=join)
        return consolidado
    except Exception as error:
        raise RuntimeError(f"Erro ({error}) ao tentar consolidar as planilhas!")