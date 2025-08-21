# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes de terceiros
import pandas as pd


def exportar_xlsx(df: pd.DataFrame, nome_arquivo: str) -> None:
    try:
        PASTA_RAIZ = Path(__file__).resolve().parents[2]
        NOME_ARQUIVO = f"{nome_arquivo}.xlsx"
        ENDERECO = PASTA_RAIZ / 'data' / 'processed' / NOME_ARQUIVO
        df.to_excel(ENDERECO, index=False, engine='openpyxl')
    except Exception as erro:
        print(f'Erro ao gerar XLSX: {erro}')  
        raise