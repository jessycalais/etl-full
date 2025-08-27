# Imports de pacotes built-in
import warnings

# Imports de pacotes pessoais
from src.extract.extract import ler_planilha
from src.transform.transform import (
    limpar_ruptura,
    limpar_estoque,
    limpar_vendas,  
    limpar_consolidado
)
from src.transform.validate import validar_df
from src.transform.merge import combinar_abas 
from src.transform.validate import (
    schema_ruptura,
    schema_estoque, 
    schema_vendas,
    validar_df
)
from src.load.to_bigquery import enviar_tabela_bq
from src.load.to_csv import exportar_csv_consolidado
from src.load.to_contact import exportar_por_cliente

# Ignorar warnings
warnings.filterwarnings("ignore")


def pipeline(base):  
  
    # EXTRACT
    # Ler as planilhas
    df_ruptura = ler_planilha(base, aba='01_BD_Ruptura_Faltaproduto')
    df_estoque = ler_planilha(base, aba='02_BD_Estoque')
    df_vendas = ler_planilha(base, aba='03_BD_Vendas')    
   
    # ===========================================================

    # TRANFORM      
    # Limpar 03 planilhas lidas
    limpar_ruptura(df_ruptura)
    limpar_estoque(df_estoque)
    limpar_vendas(df_vendas)

    # Validar os DataFrames
    validar_df(df_ruptura, schema_ruptura, log='ruptura')
    validar_df(df_estoque, schema_estoque, log='estoque')   
    validar_df(df_vendas, schema_vendas, log='vendas')

    # Consolidar os dados
    consolidado = combinar_abas(
        df_ruptura, 
        df_estoque,
        left_chave=['MES', 'COD_CLIENTE', 'MATERIAL_DESCRICAO_CATEGORIA'],
        right_chave=['MES', 'COD_CLIENTE', 'DESCRICAO_CATEGORIA'],
        join='outer'
    )

    consolidado = combinar_abas(
        consolidado,
        df_vendas,
        left_chave=['MES', 'COD_CLIENTE'],
        right_chave=['MES', 'COD_CLIENTE'],
        join='outer'
    )

    # Limpar os dados consolidados
    consolidado = limpar_consolidado(consolidado)

    # ===========================================================

    # LOAD
    # Exportar para o BigQuery
    enviar_tabela_bq(df_ruptura, 'ruptura_faltaproduto')
    enviar_tabela_bq(df_estoque, 'estoque')
    enviar_tabela_bq(df_vendas, 'vendas')
    enviar_tabela_bq(consolidado, 'consolidado')

    return consolidado