## **ETAPA 01**

#### **1.1. ETL**
- Carregar as bases;  
- Unificar arquivos e salvar em .csv;
- Validar com Pandera>
> - ColunaH = Coluna E/Coluna F
- Ingestão no BigQuery das $04$ tabelas; 
> Optamos pela `google-cloud-bigquery` porque é a lib oficial do Google, uma outra opção seria usar a lib `pandas-gbq`.
- Automatizar processo de divisão das tabelas (.csv??) para dividir por cliente e salvar num diretorio (salvar no drive ou localmente?)

#### **1.2. O que não esquecer?**
- Doc string;
- Type notation;
- Venv;
- Git e GitHub;
- Taskpy pra automatizar a divisão dos arquivos e salvamento num diretório (simplificar comando);
- Usar funções;
- Se possível, usar logging.

#### **1.3. Pastas/arquivos**
- app > tools, etl
- tools > loggers (se usar);
- app/Extract: lê arquivos (verifica as colunas existentes e esperadas já)
- app/Transform: unifica, valida e divide por usuário; 
- app/Load: envia para o BQ, para os diretorios e o unificado em `.csv`;
- logs;
- data (raw e processed);
- Criar main.py usando as funções do ETL.


#### **1.4. Possibilidades**
- App em Streamlit que recebe 3 arquivos, unifica, valida e envia pro diretório;
- App em Streamlit para cadastro dos dados. 

---

## **ETAPA 02**

#### **2.1 ...**  

