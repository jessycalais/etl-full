# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes built-in
import pandas as pd

# Imports de pacotes pessoais
from app.utils.log import (
    logger, 
    log
)

@log
def ler_planilha(endereco: Path, aba: str) -> pd.DataFrame:
    try:
        planilha = pd.read_excel(endereco, sheet_name=aba) 
        logger.info(f'Planilha "{aba}" lida com sucesso.')
        return planilha
    except Exception as error:
        logger.error(f'Erro ao ler a planilha "{aba}": {error}')
        raise RuntimeError(f'Erro ({error}) ao tentar ler a planilha!') 