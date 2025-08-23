/* Perguntas de Negócio */

/* ============================================================== */
/* QUESTÃO 01. Quais são os 5 clientes com maior valor total de ruptura (Valor Ruptura_$) no período analisado?*/
SELECT  
    CLIENTE_DESCRICAO AS NOME_CLIENTE,
    ROUND(SUM(VALOR_RUPTURA_MONETARIO), 4) AS TOTAL_RUPTURA
FROM 
    `casegb-469522.varejo.ruptura_faltaproduto`
GROUP BY
    CLIENTE_DESCRICAO
ORDER BY 
    SUM(VALOR_RUPTURA_MONETARIO) DESC
LIMIT
    5;

/* ============================================================== */
/* QUESTÃO 02. No mês mais recente, qual é a categoria de produto com a maior cobertura média de estoque?*/
SELECT
    MAX(MES) AS MES_MAIS_RECENTE,
    DESCRICAO_CATEGORIA,
    ROUND(AVG(COBERTURA_DIAS), 4) AS MEDIA_COBERTURA
FROM 
    `casegb-469522.varejo.estoque`
-- Filtrar assim para garantir que o maior mês será usado, sem a necessidade de dizer que é o mês de julho
WHERE
-- Usar CAST(MES AS INT64) apenas se mês for do tipo texto. Ajustei tipo na "Transformação" no ETL
    MES IN (
        SELECT
            MAX(MES) AS MES_MAIS_RECENTE
        FROM
            `casegb-469522.varejo.estoque`
    )
GROUP BY
    DESCRICAO_CATEGORIA
ORDER BY
    3 DESC
LIMIT 1;

/* ============================================================== */
/* QUESTÃO 03.	Qual foi o mês com o maior volume total de vendas (VLR_VOLUME_REAL)?*/
SELECT
    CASE MES
        WHEN 1 THEN 'Janeiro'
        WHEN 2 THEN 'Fevereiro'
        WHEN 3 THEN 'Março'
        WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Maio'
        WHEN 6 THEN 'Junho'
        WHEN 7 THEN 'Julho'
        WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Setembro'
        WHEN 10 THEN 'Outubro'
        WHEN 11 THEN 'Novembro'
        WHEN 12 THEN 'Dezembro'
    END MES,
    SUM(VLR_VOLUME_REAL) AS VOLUME_TOTAL
FROM 
    `casegb-469522.varejo.vendas`
GROUP BY
    MES
ORDER BY
    SUM(VLR_VOLUME_REAL) DESC
LIMIT 1;

/* ============================================================== */
/* QUESTÃO 04.	Levante uma lista de clientes que, no último mês disponível na base, 
tiveram uma taxa de ruptura (Ruptura_%) e uma cobertura de estoque em um nível que 
pode representar um risco para o negócio. (fique livre para determinar os níveis de risco) */
/*  --------- */
--JUSTIFICATIVA:
-- i. Ruptura escolhida: risco se maior do que 10%. O critério foi escolhido com fundamentação teórica. 
-- Veja dissertação de Mestrado "A REAÇÃO DO CONSUMIDOR FRENTE À RUPTURA NO VAREJO": 
-- https://repositorio.fgv.br/server/api/core/bitstreams/be9ca766-e095-46af-98e1-3a8ea96b3d31/content;
-- ii. Cobertura Média em Risco: menor do que 15 dias. Fiz essa escolha supondo que os produtos são abastecidos 
-- a cada duas semanas.


WITH ruptura_mediana_por_cliente AS (
    SELECT DISTINCT
        CLIENTE_DESCRICAO,
        PERCENTILE_CONT(RUPTURA_PERCENTUAL, 0.5) OVER(PARTITION BY CLIENTE_DESCRICAO) AS RUPTURA_MEDIANA_POR_CLIENTE
    FROM 
        `varejo.ruptura_faltaproduto`
    WHERE 
        MES = (SELECT MAX(MES) FROM `varejo.ruptura_faltaproduto`)
),
cobertura_mediana_por_cliente AS (
    SELECT DISTINCT
        NOME_CLIENTE,
        PERCENTILE_CONT(COBERTURA_DIAS, 0.5) OVER(PARTITION BY NOME_CLIENTE) AS COBERTURA_MEDIANA_POR_CLIENTE
    FROM 
        `varejo.estoque`
    WHERE 
        MES = (SELECT MAX(MES) FROM `varejo.estoque`)
)
SELECT
    r.CLIENTE_DESCRICAO,
    r.RUPTURA_MEDIANA_POR_CLIENTE,
    c.COBERTURA_MEDIANA_POR_CLIENTE      
FROM 
    ruptura_mediana_por_cliente r
    JOIN cobertura_mediana_por_cliente c
    ON r.CLIENTE_DESCRICAO = c.NOME_CLIENTE
WHERE
    r.RUPTURA_MEDIANA_POR_CLIENTE >= (
        SELECT 
            PERCENTILE_CONT(RUPTURA_PERCENTUAL, 0.5) OVER() AS RUPTURA_MEDIA_MENSAL
        FROM 
            `varejo.ruptura_faltaproduto`
        WHERE 
            MES = (SELECT MAX(MES) FROM `varejo.ruptura_faltaproduto`)
        LIMIT 1
    )
    AND c.COBERTURA_MEDIANA_POR_CLIENTE <= (
        SELECT 
            PERCENTILE_CONT(COBERTURA_DIAS, 0.5) OVER() AS COBERTURA_MEDIA_MENSAL
        FROM 
            `varejo.estoque`
        WHERE 
            MES = (SELECT MAX(MES) FROM `varejo.estoque`)
        LIMIT 1
    )
ORDER BY CLIENTE_DESCRICAO;