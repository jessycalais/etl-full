# Imports de pacotes built-in
import datetime
from io import BytesIO
from zipfile import ZipFile

# Imports de pacotes de terceiros
import pandas as pd
import streamlit as st

# Imports de pacotes pessoais
from src.utils.log import logger


def exportar_por_cliente(df: pd.DataFrame, nome_zip: str = 'clientes.zip') -> None:
    DATA = datetime.date.today().strftime('%d-%m-%Y')

    try:
        zip_buffer = BytesIO()
        clientes = df['COD_CLIENTE'].unique()

        with ZipFile(zip_buffer, 'w') as zip_file:
            for codigo_cliente in clientes:
                df_cliente = df[df['COD_CLIENTE'] == codigo_cliente]
                if df_cliente.empty:
                    continue

                csv_buffer = BytesIO()
                df_cliente.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                csv_buffer.seek(0)

                NOME_ARQUIVO = f'{codigo_cliente}_{DATA}.csv'
                zip_file.writestr(NOME_ARQUIVO, csv_buffer.read())

        zip_buffer.seek(0)

        st.download_button(
            label='Baixar pasta _zipada_ com arquivos filtrados por _Cliente/Contato_',
            data=zip_buffer.getvalue(),
            file_name=nome_zip,
            mime='application/zip'
        )

        logger.info(f'ZIP com todos os clientes gerado com sucesso: {nome_zip}')

    except Exception as erro:
        logger.error(f'Erro ao gerar ZIP de clientes: {erro}')
        raise