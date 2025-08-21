# Imports de pacotes built-in
import warnings

# Imports de pacotes de terceiros
from google.cloud import bigquery
import pandas as pd

# Ignorar warnings
warnings.filterwarnings("ignore")

def _criar_conexao_bq():
    cliente = bigquery.Client.from_service_account_json('credentials.json')

    return cliente


def _criar_dataset(cliente, id_dataset):
    dataset = bigquery.Dataset(id_dataset)
    dataset.location = 'southamerica-east1'
    cliente.create_dataset(dataset, exists_ok=True)
    # return dataset


def enviar_tabela_bq(df: pd.DataFrame, tabela: str, id_dataset: str='casegb-469522.varejo'):
    cliente = _criar_conexao_bq()
    _criar_dataset(cliente, id_dataset)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Cria a tabela ou substitui se já existir
    )

    id_tabela = f'casegb-469522.varejo.{tabela}'
    job = cliente.load_table_from_dataframe(df, id_tabela, job_config=job_config)
    job.result()  
    print('==================================')
    print(f"Tabela '{id_tabela}' criada e dados enviados com sucesso!")