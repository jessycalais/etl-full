# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes built-in
import pandas as pd

def ler_planilha(endereco: Path, aba: str): #, colunas) -> pd.DataFrame:
    try:
        planilha = pd.read_excel(endereco, sheet_name=aba) #, usecols=colunas)
        return planilha
    except Exception as error:
        raise RuntimeError(f"Erro ({error}) ao tentar ler a planilha!")



    