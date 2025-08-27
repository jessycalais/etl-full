# Imports de pacotes de terceiros
import streamlit as st

# Imports de pacotes pessoais
from src.utils.log import log

 
def carregar_dados():
    st.markdown(
        '''
        <p style="font-size:18px;">
        <b>Este App realiza as seguintes etapas no dados carregados:</b>

        - Limpeza com `Pandas`; 

        - Validação com `Pandera`, gerando arquivos com erros encontrados, caso existam;  

        - Gera um arquivo consolidado (join): `analise_consolida.csv`;  

        - Separa em arquivos por cliente/contato;

        - Envia dados das $03$ tabelas lidas e da Análise Consolidada para o _BigQuery_.  
        </p>
        ''',
        unsafe_allow_html=True
    )

    arquivo = st.file_uploader(
        label='**Carregue aqui a base de dados**',
        type='xlsx'
    )

    return arquivo