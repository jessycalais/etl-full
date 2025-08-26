# Arquivo principal 
# Elaborado por: Jéssica Barros
# Data: outubro de 2025
# Descrição: Pipeline completo (Extraction, Transformation/Validate, Load)

# ============================================================

import streamlit as st
from app.app_streamlit import aplicar_pipeline

st.set_page_config(
    page_title="DataApp", 
    page_icon="📊",
    layout='centered'
)

st.title('📊 SuperApp')

aplicar_pipeline()

# # Imports de pacotes built-in
# from pathlib import Path
# import warnings

# # Imports de pacotes de terceiros
# import pandas as pd

# # Imports de pacotes pessoais
# from src.extract.extract import ler_planilha
# from src.transform.transform import (
#     limpar_ruptura,
#     limpar_estoque,
#     limpar_vendas,  
#     limpar_consolidado
# )
# from src.transform.validate import validar_df
# from src.transform.merge import combinar_abas 
# from src.transform.validate import (
#     schema_ruptura,
#     schema_estoque, 
#     schema_vendas,
#     validar_df
# )
# from src.load.to_bigquery import enviar_tabela_bq
# from src.load.to_csv import exportar_csv_consolidado
# from src.load.to_directory import exportar_por_cliente
# from src.load.to_xlsx import exportar_xlsx

# # Ignorar warnings
# warnings.filterwarnings("ignore")

# # ===========================================================

# # EXTRACT
# # Endereço do arquivo 
# DIRETORIO_PAI = Path(__file__).resolve().parent
# ENDERECO_ARQUIVO = DIRETORIO_PAI / 'data' / 'raw' / '02_Case_Analista de Dados_ Dados.xlsx'

# # Ler as planilhas
# df_ruptura = ler_planilha(ENDERECO_ARQUIVO, '01_BD_Ruptura_Faltaproduto')
# df_estoque = ler_planilha(ENDERECO_ARQUIVO, '02_BD_Estoque')
# df_vendas = ler_planilha(ENDERECO_ARQUIVO, '03_BD_Vendas')

# # ===========================================================

# # TRANSFORM/VALIDATE
# # Limpar as tabelas individuais
# limpar_ruptura(df_ruptura)
# limpar_estoque(df_estoque)
# limpar_vendas(df_vendas)

# # Validar os DataFrames
# validar_df(df_ruptura, schema_ruptura, log='ruptura')
# validar_df(df_estoque, schema_estoque, log='estoque')   
# validar_df(df_vendas, schema_vendas, log='vendas')

# # Consolidar os dados
# consolilado = combinar_abas(
#     df_ruptura, 
#     df_estoque,
#     left_chave=['MES', 'COD_CLIENTE', 'MATERIAL_DESCRICAO_CATEGORIA'],
#     right_chave=['MES', 'COD_CLIENTE', 'DESCRICAO_CATEGORIA'],
#     join='outer'
# )

# consolilado = combinar_abas(
#     consolilado,
#     df_vendas,
#     left_chave=['MES', 'COD_CLIENTE'],
#     right_chave=['MES', 'COD_CLIENTE'],
#     join='outer'
# )

# # Limpar os dados consolidados
# consolilado = limpar_consolidado(consolilado)

# # ===========================================================

# # LOAD
# # Exportar consolidado para arquivo consolidado no formato CSV
# exportar_csv_consolidado(consolilado, 'analise_consolidada')

# # Exportar por cliente
# exportar_por_cliente(consolilado)

# # Exportar tabelas individuais no formato xlsx
# exportar_xlsx(df_ruptura, 'ruptura_faltaproduto')
# exportar_xlsx(df_estoque, 'estoque')    
# exportar_xlsx(df_vendas, 'vendas')

# # Exportar para o BigQuery
# enviar_tabela_bq(df_ruptura, 'ruptura_faltaproduto')
# enviar_tabela_bq(df_estoque, 'estoque')
# enviar_tabela_bq(df_vendas, 'vendas')
# enviar_tabela_bq(consolilado, 'consolidado')