# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes de terceiros
import pandas as pd

# Imports de pacotes pessoais
from src.utils.log import (
    logger, 
    log
)

@log
def exportar_csv_consolidado(df: pd.DataFrame, nome_arquivo: str) -> None:
    try:
        PASTA_RAIZ = Path(__file__).resolve().parents[2]
        NOME_ARQUIVO = f"{nome_arquivo}.csv"
        ENDERECO = PASTA_RAIZ / 'data' / 'processed' / NOME_ARQUIVO
        df.to_csv(ENDERECO, index=False, encoding='utf-8-sig') 
        logger.info(f'Arquivo consolidado exportado com sucesso: {ENDERECO}')
    except Exception as erro:
        logger.error(f'Erro ao exportar arquivo consolidado: {erro}')
        print(f'Erro ao exportar arquivo consolidado: {erro}')  
        raise