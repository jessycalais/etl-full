# Imports de pacotes built-in
import warnings

# Imports de pacotes de terceiros
from google.cloud import bigquery
import pandas as pd

# Imports de pacotes pessoais
from src.utils.log import (
    logger, 
    log
)

# Ignorar warnings
warnings.filterwarnings("ignore")


def _criar_conexao_bq() -> bigquery.Client | None:
    cliente = bigquery.Client.from_service_account_json('credentials.json')
    logger.info('Conexão com BigQuery criada com sucesso!')
    return cliente

@log
def _criar_dataset(cliente, id_dataset) -> None:
    try:
        dataset = bigquery.Dataset(id_dataset)
        dataset.location = 'southamerica-east1'
        cliente.create_dataset(dataset, exists_ok=True)
        logger.info(f'Dataset {id_dataset} criado ou já existente.')
    except Exception as erro:
        logger.error(f'Erro ao criar dataset: {erro}')

@log
def enviar_tabela_bq(df: pd.DataFrame, tabela: str, id_dataset: str='poetic-standard-439816-e6.varejo'):
    cliente = _criar_conexao_bq()
    if cliente is None:
        logger.error('Não foi possível criar a conexão com o BigQuery.')
        # Para interromper a execução
        raise RuntimeError('Falha na conexão com o BigQuery!')

    _criar_dataset(cliente, id_dataset)

    try: 
        job_config = bigquery.LoadJobConfig(
            write_disposition='WRITE_TRUNCATE',  # Cria a tabela ou substitui se já existir
        )
        id_tabela = f'poetic-standard-439816-e6.varejo.{tabela}'
        job = cliente.load_table_from_dataframe(df, id_tabela, job_config=job_config)
        job.result()  
        print('==================================')
        print(f'Tabela "{id_tabela}" criada e dados enviados com sucesso!')
        logger.info(f'Tabela "{id_tabela}" criada e dados enviados com sucesso!')
    except Exception as erro:
        logger.error(f'Erro ao enviar dados para o BigQuery: {erro}')