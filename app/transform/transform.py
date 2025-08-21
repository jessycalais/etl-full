# Imports de pacotes de terceiros
import numpy as np
import pandas as pd

# ----------------------------------------------------
# GERAL
def _separar_ano_mes(df: pd.DataFrame, coluna_data: str, num_digitos: int) -> pd.DataFrame:
    df[coluna_data] = df[coluna_data].astype(str).str.zfill(num_digitos)
    df['ANO'] = df[coluna_data].str[:4]
    df['MES'] = df[coluna_data].str[4:]
    df.drop(columns=coluna_data, inplace=True)
    df.insert(0, 'ANO', df.pop('ANO'))
    df.insert(1, 'MES', df.pop('MES'))

    return df

def _coletar_mes(df: pd.DataFrame, coluna_mes: str, num_digitos: int) -> pd.DataFrame:
    df[coluna_mes].astype(str).str.zfill(num_digitos)
    df[coluna_mes]=df[coluna_mes].str[1:]   

    return df


def _renomear_colunas(df: pd.DataFrame, colunas: dict) -> pd.DataFrame:
    df.rename(columns=colunas, inplace=True)
    
    return df


def _converter_letras_maiusculas(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    for coluna in colunas:
        df[coluna] = df[coluna].str.upper()
    
    return df


def _remover_colunas(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    df.drop(columns=colunas, inplace=True)

    return df


def _definir_tipos(df: pd.DataFrame, tipos: dict) -> pd.DataFrame:
    for coluna, tipo in tipos.items():
        df[coluna] = df[coluna].astype(tipo)
    
    return df

def _inserir_ano_estoque(df: pd.DataFrame, ano: int) -> pd.DataFrame:
    df['ANO'] = ano

    return df


# ----------------------------------------------------
# RUPTURA
def _converter_valor_monetario(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    df[coluna]= df[coluna].astype(str).str.replace('R$ ', '', regex=False)
    df[coluna] = df[coluna].astype(str).str.replace('.', '', regex=False)
    df[coluna] = df[coluna].astype(str).str.replace(',', '.', regex=False)
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    return df


def _ajustar_ruptura_percentual(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    df.loc[df["VALOR_PEDIDO_MONETARIO"].isna(), "RUPTURA_PERCENTUAL"] = np.nan
    df.loc[df["VALOR_PEDIDO_MONETARIO"] == 0, "RUPTURA_PERCENTUAL"] = np.nan

    return df


def _remover_hifen(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    for coluna in colunas:
        df[coluna] = df[coluna].replace('-', np.nan, regex=False)
    
    return df


def limpar_ruptura(df: pd.DataFrame) -> pd.DataFrame:
    df = (df.pipe(_separar_ano_mes, coluna_data='DT_MES', num_digitos=6)
        .pipe(_converter_valor_monetario, coluna='Valor Ruptura_$')
        .pipe(_converter_valor_monetario, coluna='Valor Pedido_$')
        .pipe(_remover_hifen, colunas=['Valor Ruptura_$', 'Valor Pedido_$'])
        .pipe(_renomear_colunas, colunas={
            'Valor Ruptura_$': 'VALOR_RUPTURA_MONETARIO',
            'Valor Pedido_$': 'VALOR_PEDIDO_MONETARIO',
            'Volume ruptura_und': 'VOLUME_RUPTURA_UND',
            'Ruptura_%': 'RUPTURA_PERCENTUAL'
        })
        .pipe(_ajustar_ruptura_percentual, colunas=['VALOR_PEDIDO_MONETARIO', 'RUPTURA_PERCENTUAL'])
    )

    return df

# ----------------------------------------------------
# ESTOQUE
def limpar_estoque(df: pd.DataFrame) -> pd.DataFrame:
    df = (df.pipe(_coletar_mes, coluna_mes='MES', num_digitos=3)
        .pipe(_renomear_colunas, colunas={
            'NOME CLIENTE': 'NOME_CLIENTE',
            'CONTATO CLIENTE': 'CONTATO_CLIENTE'
        })
        .pipe(_converter_letras_maiusculas, colunas=['CONTATO_CLIENTE'])
    )

    return df

# ----------------------------------------------------
# VENDAS
def limpar_vendas(df: pd.DataFrame) -> pd.DataFrame:
    df = (df.pipe(_separar_ano_mes, coluna_data='DT_MES', num_digitos=6)
        .pipe(_renomear_colunas, colunas={
            'COD CLIEN': 'COD_CLIENTE'
        })
    )

    return df


# ----------------------------------------------------
# CONSOLIDADO
def _definir_tipos_consolidado(df: pd.DataFrame) -> pd.DataFrame: 
    tipos = {
        'ANO': 'int',
        'MES': 'int',
        'COD_CLIENTE': 'str',
        'CLIENTE_DESCRICAO': 'str',
        'MATERIAL_DESCRICAO_CATEGORIA': 'str',
        'VALOR_RUPTURA_MONETARIO': 'float',
        'VALOR_PEDIDO_MONETARIO': 'float',
        'VOLUME_RUPTURA_UND': 'Int64',
        'RUPTURA_PERCENTUAL': 'float',
        'ESTOQUE': 'Int64',
        'DDV': 'float',
        'COBERTURA_DIAS': 'Int64',
        'TIPO_CLIENTE': 'str',
        # 'CONTATO_CLIENTE': 'str',
        'VLR_VOLUME_REAL': 'Int64',
        'CIDADE': 'str',
        'UF': 'str',
        'PAIS': 'str'      
    }

    df = _definir_tipos(df, tipos)

    return df


def limpar_consolidado(df: pd.DataFrame) -> pd.DataFrame:
    # A função `_converter_letras_maiusculas` poderia ser usada aqui em todas as colunas do tipo texto
    df = (df.pipe(_remover_colunas, colunas=['ANO_y', 'NOME_CLIENTE', 'DESCRICAO_CATEGORIA'])
        .pipe(_renomear_colunas, colunas={'ANO_x': 'ANO'})
        .pipe(_inserir_ano_estoque, ano=2021)
        .pipe(_definir_tipos_consolidado)
    )

    return df


# TO-DO
















