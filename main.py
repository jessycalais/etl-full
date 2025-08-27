# Arquivo principal 
# Elaborado por: Jéssica Barros
# Data: outubro de 2025
# Descrição: Aplicação do Pipeline, Tela do Streamlit e Botões de Download

# ============================================================

# Imports de pacotes de terceiros
import streamlit as st

# Imports de pacotes pessoais
from src.load.to_contact import exportar_por_cliente
from src.load.to_csv import exportar_csv_consolidado
from src.utils.app_streamlit import carregar_dados
from src.utils.log import (
    get_log_contents,
    clear_log
)
from src.pipeline import pipeline


st.set_page_config(
    page_title='SuperApp', 
    page_icon='📊',
    layout='centered'
)

st.title('📊 SuperApp')


if "pipeline_sucesso" not in st.session_state:
    st.session_state.pipeline_sucesso = False
if "consolidado" not in st.session_state:
    st.session_state.consolidado = None
if "mostrar_logs" not in st.session_state:
    st.session_state.mostrar_logs = False

# Serve para não aplicar o Pipeline de novo ao clicar nos botões de download ou log
@st.cache_data(show_spinner=False)
def consolidar_dados_cache(arquivo):
    return pipeline(base=arquivo)  

arquivo = carregar_dados()

if arquivo:
    with st.spinner('Aplicando Pipeline ... Aguarde!'):
        try:
            st.session_state.consolidado = consolidar_dados_cache(arquivo)
        except Exception as e:
            st.error('Não foi possível realizar o Pipeline completo.')
        else:
            st.success('Pipeline concluído!')
            st.session_state.pipeline_sucesso = True 


if st.session_state.pipeline_sucesso and st.session_state.consolidado is not None:
    exportar_csv_consolidado(df=st.session_state.consolidado, nome_arquivo='analise_consolidada')
    exportar_por_cliente(df=st.session_state.consolidado)


exibir_logs = st.checkbox(label='Exibir logs!')

if exibir_logs:
    st.text_area(
        'Logs do Pipeline',
        value=get_log_contents(),
        height=300
    )

    clear_log()