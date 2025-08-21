# Imports de pacotes built-in
import datetime
from pathlib import Path

# Imports de pacotes de terceiros
import pandas as pd


def _filtrar_cliente(df):
    codigos = df['COD_CLIENTE'].unique().tolist()
    planilhas_individuais = []
    for codigo in codigos:
        df_filtrado = df[df['COD_CLIENTE'] == codigo]
        planilhas_individuais.append((codigo, df_filtrado))

    return planilhas_individuais


def exportar_por_cliente(df: pd.DataFrame) -> None:
    planilhas_individuais = _filtrar_cliente(df)
    PASTA_RAIZ = Path(__file__).resolve().parents[2]
    DATA = datetime.date.today().strftime("%d-%m-%Y")
    try:
        for codigo_cliente, df_cliente in planilhas_individuais:
            indice = df_cliente[
                (df_cliente['COD_CLIENTE'] == codigo_cliente) &
                (df_cliente['CONTATO_CLIENTE'].notna())
            ].index
            contato_cliente = df_cliente.loc[indice, 'CONTATO_CLIENTE'].iloc[0]
            NOME_ARQUIVO = f'{codigo_cliente}_{contato_cliente}_{DATA}.csv'
            ENDERECO = PASTA_RAIZ / 'data' / 'by_client' / NOME_ARQUIVO
            df_cliente.to_csv(ENDERECO, index=False, encoding='utf-8-sig') 
    
    except Exception as erro:
        print(f'Erro ao salvar planilhas: {erro}')
        raise