----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Consulta para verificar o ranking dos funcionarios agrupamento por departamento e ordendo do maior para o menor de cada departamento
SELECT 
    departamento,
    nome_completo,
    salario,
    RANK() OVER (
        PARTITION BY departamento 
        ORDER BY salario DESC
    ) AS ranking_salario
FROM tabela_funcionarios
ORDER BY departamento, ranking_salario;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Consulta para separar por departamento somando os funcionarios de cada departamento e calculando o salario medio por departamento
SELECT 
    departamento,
    COUNT(*) AS total_funcionarios, -- conta quantas linhas existem em cada departamento
    ROUND(AVG(salario), 2) AS salario_medio --calcula a media salarial e arrendonda em 2 casas
FROM tabela_funcionarios
GROUP BY departamento
ORDER BY departamento;

