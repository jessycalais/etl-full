🚀 **PROJETO COMPLETO DE ETL COM CONSULTAS SQL**

**OBJETIVO:** Criar um ETL automatizado para tratamento de dados, consolidação, criação de arquivos em Excel e tabelas no BigQuery. Além disso, respondemos algumas perguntas de negócio utilizando SQL a fim de obter insights que ajudem o gestor a tomar decisões.

> TO-DO: 
> - Criação de Dashboard no `Looker Studio` conectado ao `BigQuery`;
> - Apresentação em `.ppt` para trazer os *insights* e recomendações;
> - Solução para uma problema: Gestão de Crise.

## **ETAPA 01**

### **1.1. ETL**
**1.1.1. EXTRACTION:**
- Carregar as bases: $03$ planilhas (abas) de um arquivo Excel. 

**1.1. 2. TRANSFORMATION:**
- Limpar dados (colunas, tipos, missing, etc);
- Fazer `join`para gerar consolidado e salvar em .csv;
- Validar com a lib `Pandera` (criação de schemas e função de validação).

**1.1.3. LOAD:**
- Ingestão no BigQuery das $04$ tabelas ($03$ planilhas + 1 tabela unificada):
    - Tabela 1: Ruptura;
    - Tabela 2: Estoque;
    - Tabela 3: Vendas;
    - Tabela 4: Análise Consolidada (resultado do join).
    > Optamos pela `google-cloud-bigquery` porque é a lib oficial do Google, uma outra opção seria usar a lib `pandas-gbq`.
- Automação do processo de divisão das tabelas por `COD_CLIENTE | CONTATO_CLIENTE` com opção de download;
- Salvar o arquivo unificado no formato `.csv` com opção de download.

### **1.2. Boas práticas**  
- Type notation;  
- Ambiente Virtual com Poetry;  
- Git e GitHub;  
- Funções pequenas e objetivas;  
- Validação com Pandera;  
- Logs com a lib `logging`;
- Estrutura de pastas organizada por funcionalidade (Extract, Transform, Load, Utils).

### **1.3. Estrutura do Projeto**
├── .gitignore  
├── README.md  
├── main.py  
├── poetry.lock  
├── pyproject.toml  
├── app  
│    ├── utils  
│    │  ├── __init__.py  
│    │  └── log.py  
│    ├── Extract  
│    │  ├── __init__.py  
│    │  └── extract.py  
│    ├── Transform  
│    │  ├── __init__.py  
│    │  ├── transform.py  
│    │  ├── merge.py  
│    │  └── validate.py  
│    └── Load  
│        ├── __init__.py  
│        ├── to_bigquery.py  
│        ├── to_csv.py  
│        ├── to_directory.py  
├── data  
│    ├── raw/                 # arquivos brutos originais  
│    └── processed/           # arquivos após processamento  
├── logs/                     # arquivos de log gerados  
├── consultas_sql  
│     ├── consultas_sql.sql   # arquivo com queries SQL

### **1.4. TO-DO**
- Escrever `docstring` e criar documentação com `mkdocs`;
- App em Streamlit para cadastro dos dados para garantir recebimento correto dos dados enviados por outra área.

======================

## **ETAPA 02**

### **2.1. CONSULTAS SQL PARA ANÁLISE DE VENDAS, ESTOQUE E RUPTURA**  

**2.1.1. Conceitos utilizados**
- Utilizamos a ferramenta `Google BigQuery` para realizar as consultas SQL nas tabelas carregadas na etapa anterior.;
- Conceitos utilizados:
    - `JOIN` para combinar dados de diferentes tabelas;
    - `GROUP BY` para agregar dados por categorias específicas;
    - `ORDER BY` para ordenar os resultados;
    - `WHERE` para filtrar os dados com base em condições específicas;
    - Funções de agregação como `SUM()`, `AVG()`, `PERCENTILE_CONT`;
    - `CTE (Common Table Expressions)` para organizar consultas complexas;
    - `Window Functions` para cálculos que envolvem um conjunto de linhas relacionadas;
    - `Subqueries` para consultas aninhadas;
    - Criação de `Views` para facilitar consultas futuras.

**2.2.2 Perguntas respondidas**
- **QUESTÃO 01.** Quais são os 5 clientes com maior valor total de ruptura (Valor Ruptura_$) no período analisado?

- **QUESTÃO 02.** No mês mais recente, qual é a categoria de produto com a maior cobertura média de estoque?

- **QUESTÃO 03.** Qual foi o mês com o maior volume total de vendas (VLR_VOLUME_REAL)?

- **QUESTÃO 04.** Levante uma lista de clientes que, no último mês disponível na base, tiveram uma taxa de ruptura (Ruptura_%) e uma cobertura de estoque em um nível que pode representar um risco para o negócio. (fique livre para determinar os níveis de risco).