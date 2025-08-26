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
def exportar_xlsx(df: pd.DataFrame, nome_arquivo: str) -> None:
    try:
        PASTA_RAIZ = Path(__file__).resolve().parents[2]
        NOME_ARQUIVO = f"{nome_arquivo}.xlsx"
        ENDERECO = PASTA_RAIZ / 'data' / 'processed' / NOME_ARQUIVO
        df.to_excel(ENDERECO, index=False, engine='openpyxl')
        logger.info(f'Arquivo {NOME_ARQUIVO} salvo com sucesso em {ENDERECO}!')
    except Exception as erro:
        print(f'Erro ao gerar xlsx: {erro}')  
        logger.error(f'Erro ao gerar xlsx: {erro}')
        raise