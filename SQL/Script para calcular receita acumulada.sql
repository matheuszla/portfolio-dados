------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Criaçao de um visao para facilitar a consulta da receita acumulada de 2023
CREATE VIEW view_receita_acumulada_2023 AS
SELECT
  periodo,
  SUM(vendas_atual) OVER (ORDER BY periodo) AS receita_acumulada
FROM tabela_receita_acumulada
WHERE periodo LIKE '2023-%'
ORDER BY periodo;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Query para visualizar a view
SELECT * FROM view_receita_acumulada_2023;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--Validaçao dos valores 
SELECT
  -- Soma de todos os meses de 2023 (manual)
  (SELECT SUM(vendas_atual) FROM tabela_receita_acumulada WHERE periodo LIKE '2023-%') AS soma_total,
  
  -- Receita acumulada do último mês (via view)
  (SELECT receita_acumulada FROM view_receita_acumulada_2023 ORDER BY periodo DESC LIMIT 1) AS receita_acumulada_final;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
