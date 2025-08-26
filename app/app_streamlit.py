import streamlit as st
from src.pipeline import pipeline
 
def _carregar_dados():
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

def aplicar_pipeline():
       
    arquivo = _carregar_dados()
    if arquivo:
        with st.spinner("Aplicando Pipeline ... Aguarde!"):  
            try:          
                pipeline(base=arquivo)
            except:
                st.error('Não foi possível realizar o Pipeline completo. Verifique o arquivo de _log_ para mais detalhes!')
            else:
                st.success('Arquivos enviados para o BigQuery com sucesso!')
            

           
