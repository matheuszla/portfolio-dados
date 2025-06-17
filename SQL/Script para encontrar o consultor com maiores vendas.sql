---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Criacao de uma tabela temporaria para facilitar a organizaçao dos dados
WITH ranking_vendas AS (
  SELECT    ano,    nome_consultor,    valor_venda, ROW_NUMBER() OVER (PARTITION BY ano ORDER BY valor_venda DESC) AS rn
  FROM tabela_consultores
)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Consulta principal que vai buscar apenas a linha com maior venda, ordenado por ano
SELECT  ano,  nome_consultor,  valor_venda
FROM ranking_vendas
WHERE rn = 1
ORDER BY ano;
