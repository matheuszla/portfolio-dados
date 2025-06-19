------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Contagem de contratos únicos com status 'ativo'
SELECT 
    COUNT(DISTINCT contrato_id) AS total_contratos_ativos
FROM dim_contratos
WHERE status_contrato = 'ativo';
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Calcula a média do valor financiado agrupado por cidade dos clientes
SELECT 
    c.cidade,  -- Cidade do cliente
    ROUND(AVG(ct.valor_financiado), 2) AS media_valor_financiado  -- Média arredondada para 2 casas decimais
FROM dim_contratos ct
JOIN dim_clientes c 
    ON ct.cliente_id = c.cliente_id  -- Faz o join entre contratos e clientes para pegar a cidade
GROUP BY c.cidade  -- Agrupa por cidade
ORDER BY media_valor_financiado DESC;  -- Ordena da maior para a menor média
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Seleciona as 5 cidades que possuem o maior número de contratos
SELECT 
    c.cidade,  -- Cidade do cliente
    COUNT(ct.contrato_id) AS quantidade_contratos  -- Contagem de contratos por cidade
FROM dim_contratos ct
JOIN dim_clientes c 
    ON ct.cliente_id = c.cliente_id
GROUP BY c.cidade  -- Agrupa por cidade
ORDER BY quantidade_contratos DESC  -- Ordena da maior quantidade para a menor
LIMIT 5;  -- Limita o resultado aos 5 primeiros
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Conta quantos contratos estão com status 'inadimplente'
SELECT 
    COUNT(*) AS total_inadimplentes
FROM dim_contratos
WHERE status_contrato = 'inadimplente';
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Lista os clientes que possuem:
-- - idade maior que 50 anos
-- - contratos ativos
-- - e prazo acima de 180 meses

SELECT 
    c.cliente_id,    -- ID do cliente
    c.nome,          -- Nome do cliente
    c.idade,         -- Idade do cliente
    ct.contrato_id,  -- ID do contrato
    ct.prazo_meses,  -- Prazo do contrato em meses
    ct.status_contrato  -- Status do contrato
FROM dim_contratos ct
JOIN dim_clientes c 
    ON ct.cliente_id = c.cliente_id
WHERE 
    c.idade > 50  -- Filtra clientes com mais de 50 anos
    AND ct.status_contrato = 'ativo'  -- Somente contratos ativos
    AND ct.prazo_meses > 180;  -- E com prazo superior a 180 meses
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Soma o valor total de pagamentos realizados, agrupado por cidade dos clientes
SELECT 
    c.cidade,  -- Cidade do cliente
    ROUND(SUM(p.valor_pago), 2) AS total_pago  -- Soma dos pagamentos, arredondada para 2 casas decimais
FROM fato_pagamentos p
JOIN dim_contratos ct 
    ON p.contrato_id = ct.contrato_id
JOIN dim_clientes c 
    ON ct.cliente_id = c.cliente_id
GROUP BY c.cidade  -- Agrupa por cidade
ORDER BY total_pago DESC;  -- Ordena do maior total de pagamento para o menor
