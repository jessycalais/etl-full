# Imports de pacotes de terceiros
import pandas as pd
import streamlit as st
from pandera.pandas import (
    Column, 
    DataFrameSchema, 
    Check, 
    errors
)

# Imports de pacotes pessoais
from src.utils.log import logger

# SCHEMAS DE VALIDAÇÃO
schema_ruptura = DataFrameSchema({
    'ANO': Column(
        int, 
        # Posssibilidade de inserir novos anos
        Check.isin([2021]), # Retirei aspas
        nullable=True
    ),
    'MES': Column(
        int, 
        Check.in_range(1, 12),
        nullable=True # Verificar
    ),
    'COD_CLIENTE': Column(
        str, 
        Check.str_length(2)
    ),  
    'CLIENTE_DESCRICAO': Column(
        str, 
        Check.str_length(1, 100)
    ),
    'MATERIAL_DESCRICAO_CATEGORIA': Column(
        str, 
        Check.str_length(1, 100)
    ),  
    'VALOR_RUPTURA_MONETARIO': Column(
        float, 
        Check.greater_than_or_equal_to(0),
        nullable=True
    ),
    'VALOR_PEDIDO_MONETARIO': Column(
        float, 
        Check.greater_than_or_equal_to(0),
        nullable=True
    ),
    'VOLUME_RUPTURA_UND': Column(
        int, 
        Check.greater_than_or_equal_to(0)
    ),
    'RUPTURA_PERCENTUAL': Column(
        float, 
        Check.greater_than_or_equal_to(0),
        nullable=True
    )
})

schema_estoque = DataFrameSchema({
    'MES': Column(
        int, 
        Check.in_range(1, 12)
    ),
    'COD_CLIENTE': Column(
        str, 
        Check.str_length(2)
    ),
    'NOME_CLIENTE': Column(
        str, 
        Check.str_length(1, 100)
    ),
    'DESCRICAO_CATEGORIA': Column(
        str, 
        Check.str_length(1, 100)
    ),
    'ESTOQUE': Column(
        int, 
        Check.greater_than_or_equal_to(0),
        nullable=True
    ),
    'DDV': Column(
        float, 
        Check.greater_than_or_equal_to(0),
        nullable=True
    ),
    'COBERTURA_DIAS': Column(
        int, 
        Check.greater_than_or_equal_to(0)
    ),
    'TIPO_CLIENTE': Column(
        str, 
        Check.isin(['ESPECIAL', 'PADRÃO'])
    ),
    'CONTATO_CLIENTE': Column(
        str, 
        Check.str_length(1, 100)
    )
})

schema_vendas = DataFrameSchema({
    'ANO': Column(
        int,
        Check.isin([2021]), # Atencao, retirei aspas
        nullable=True
    ),      
    'MES': Column(
        int, 
        Check.in_range(1, 12),
        nullable=True
    ),  
    'COD_CLIENTE': Column(
        str,            
        Check.str_length(2)
    ),      
    'VLR_VOLUME_REAL': Column(
        int,
        Check.greater_than_or_equal_to(0)
    ),
    'CIDADE': Column(   
        str, 
        Check.str_length(1, 100)
    ),
    'UF': Column(
        str, 
        Check.isin(['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 
                'MA','MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 
                'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
        ])
    ),
    'PAIS': Column(
        str, 
        Check.isin(['BR'])
    )
})


# Função para validar DataFrame
def validar_df(df: pd.DataFrame, schema, log) -> pd.DataFrame | None:
    try:
        validate_df = schema.validate(df, lazy=True)
        logger.info(f'DataFrame validado com sucesso: {log}!')
        return validate_df    
    except errors.SchemaErrors as erro:
        logger.error(f'Erros encontrados na validação do DataFrame: {log}!')
        NOME_ARQUIVO = f'erros_validacao_{log}.csv'
    
        # Gerar csv com os erros
        erros_df = erro.failure_cases
        csv_bytes = erros_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=f'Baixar erros de validação ({log})',
            data=csv_bytes,
            file_name=NOME_ARQUIVO,
            mime='text/csv'
        )
        
        raise RuntimeError(f'Erros encontrados na validação do DataFrame: {log}!')