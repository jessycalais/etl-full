# Imports de pacotes built-in
from pathlib import Path

# Imports de pacotes de terceiros
import pandas as pd
from pandera.pandas import (
    Column, 
    DataFrameSchema, 
    Check, 
    errors
)

# Imports de pacotes pessoais
from app.utils.log import (
    logger, 
    log
)

# SCHEMAS DE VALIDAÇÃO
schema_ruptura = DataFrameSchema({
    'ANO': Column(
        int, 
        # Posssibilidade de inserir novos anos
        Check.isin(['2021']),
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
        Check.isin(['2021']),
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
@log
def validar_df(df: pd.DataFrame, schema, log) -> pd.DataFrame | None:
    try:
        validate_df = schema.validate(df, lazy=True)
        logger.info(f'DataFrame validado com sucesso: {log}!')
        return validate_df    
    except errors.SchemaErrors as erro:
        print('==================================')
        print(f'Erros encontrados na validação do DataFrame: {log}!')
        logger.error(f'Erros encontrados na validação do DataFrame: {log}!')
        PASTA_RAIZ = Path(__file__).resolve().parents[2]
        NOME_ARQUIVO = f'erros_validacao_{log}.csv'
        ENDERECO = PASTA_RAIZ / 'logs' / NOME_ARQUIVO
        erro.failure_cases.to_csv(ENDERECO, index=False)
        print(f'Log de erros de validação do DataFrame salvo em: {ENDERECO}.')