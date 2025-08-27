# Imports de pacotes de terceiros
import pandas as pd

# Imports de pacotes pessoais
from src.utils.log import logger


def combinar_abas(df1: pd.DataFrame, df2: pd.DataFrame, left_chave, right_chave, join): 
    try:
        consolidado = pd.merge(df1, df2, left_on=left_chave, right_on=right_chave, how=join)
        logger.info('Planilhas combinadas (join) com sucesso!')
        return consolidado
    except Exception as error:
        logger.error(f'Erro ao tentar combinar (join) as planilhas: {error}')
        raise RuntimeError(f'Erro ({error}) ao tentar consolidar as planilhas!')