/* Perguntas de Negócio */

/* ============================================================== */

/* QUESTÃO 01. Quais são os 5 clientes com maior valor total de ruptura (Valor Ruptura_$) no período analisado? */
SELECT  
    COD_CLIENTE AS CODIGO_CLIENTE,
    SUM(VALOR_RUPTURA_MONETARIO) AS TOTAL_RUPTURA
FROM `casegb-469522.varejo.ruptura_faltaproduto`
GROUP BY
    COD_CLIENTE 
ORDER BY 
    SUM(VALOR_RUPTURA_MONETARIO) DESC
LIMIT
    5;

/* ============================================================== */

/*  QUESTÃO 02.	No mês mais recente, qual é a categoria de produto com a maior cobertura média de estoque? */
SELECT
    DESCRICAO_CATEGORIA,
    AVG(COBERTURA_DIAS) AS MEDIA_COBERTURA
FROM `casegb-469522.varejo.estoque`
-- Filtrar assim para garantir que o maior mês será usado, sem a necessidade de dizer que é '07'
WHERE
    CAST(MES AS INT64) IN (
         SELECT
            MAX(CAST(MES AS INT64)) AS MAIOR_MES
        FROM
            `casegb-469522.varejo.estoque`
    )
GROUP BY
    DESCRICAO_CATEGORIA
ORDER BY
    2 DESC
LIMIT 1;

/* ============================================================== */

/* QUESTÃO 03.	Qual foi o mês com o maior volume total de vendas (VLR_VOLUME_REAL)? */
SELECT
    CASE MES
        WHEN '01' THEN 'Janeiro'
        WHEN '02' THEN 'Fevereiro'
        WHEN '03' THEN 'Março'
        WHEN '04' THEN 'Abril'
        WHEN '05' THEN 'Maio'
        WHEN '06' THEN 'Junho'
        WHEN '07' THEN 'Julho'
        WHEN '08' THEN 'Agosto'
        WHEN '09' THEN 'Setembro'
        WHEN '10' THEN 'Outubro'
        WHEN '11' THEN 'Novembro'
        WHEN '12' THEN 'Dezembro'
    END MES,
    SUM(VLR_VOLUME_REAL) AS VOLUME_TOTAL
FROM `casegb-469522.varejo.vendas`
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
/* --------- */
SELECT  
    COD_CLIENTE,
    CLIENTE_DESCRICAO,
    MATERIAL_DESCRICAO_CATEGORIA AS CATEGORIA,
    RUPTURA_PERCENTUAL,
    COBERTURA_DIAS
FROM
    `casegb-469522.varejo.consolidado`
WHERE
    RUPTURA_PERCENTUAL > 0.1
    AND COBERTURA_DIAS < 15
ORDER BY
    COD_CLIENTE,
    CATEGORIA;