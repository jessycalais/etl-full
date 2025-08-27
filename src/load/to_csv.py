# Imports de pacotes de terceiros
from io import BytesIO
import pandas as pd
import streamlit as st

# Imports de pacotes pessoais
from src.utils.log import logger


def exportar_csv_consolidado(df: pd.DataFrame, nome_arquivo: str) -> None:
    try:
        NOME_ARQUIVO = f'{nome_arquivo}.csv'
        buffer = BytesIO()
        df.to_csv(buffer, index=False, encoding='utf-8-sig')
        buffer.seek(0)
        st.download_button(
            label='Baixar _Análise Consolidada_',
            data=buffer.getvalue(),
            file_name=NOME_ARQUIVO,
            mime="text/csv"
        )
        logger.info('Arquivo consolidado gerado com sucesso!')
    except:
        logger.error('Não foi possível gerar o arquivo consolidado!')