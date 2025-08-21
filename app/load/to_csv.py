# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes de terceiros
import pandas as pd


def exportar_csv_consolidado(df: pd.DataFrame, nome_arquivo: str) -> None:
    try:
        PASTA_RAIZ = Path(__file__).resolve().parents[2]
        NOME_ARQUIVO = f"{nome_arquivo}.csv"
        ENDERECO = PASTA_RAIZ / 'data' / 'processed' / NOME_ARQUIVO
        df.to_csv(ENDERECO, index=False, encoding='utf-8-sig') 
    except Exception as erro:
        print(f'Erro ao gerar CSV: {erro}')  
        raise