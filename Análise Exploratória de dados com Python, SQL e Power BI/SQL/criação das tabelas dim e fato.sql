-- Clientes
CREATE TABLE dim_clientes (
    cliente_id TEXT PRIMARY KEY,
    nome TEXT,
    idade REAL,
    renda_mensal REAL,
    cidade TEXT
);

-- Contratos
CREATE TABLE dim_contratos (
    contrato_id TEXT PRIMARY KEY,
    cliente_id TEXT,
    valor_financiado REAL,
    data_contrato TEXT,
    prazo_meses REAL,
    status_contrato TEXT,
    FOREIGN KEY (cliente_id) REFERENCES dim_clientes(cliente_id)
);

-- Pagamentos
CREATE TABLE fato_pagamentos (
    pagamento_id TEXT PRIMARY KEY,
    contrato_id TEXT,
    data_pagamento TEXT,
    valor_pago REAL,
    FOREIGN KEY (contrato_id) REFERENCES dim_contratos(contrato_id)
);



-- Populando dim_clientes
INSERT INTO dim_clientes (cliente_id, nome, idade, renda_mensal, cidade)
SELECT cliente_id, nome, idade, renda_mensal, cidade
FROM clientes;

-- Populando dim_contratos
INSERT INTO dim_contratos (contrato_id, cliente_id, valor_financiado, data_contrato, prazo_meses, status_contrato)
SELECT contrato_id, cliente_id, valor_financiado, data_contrato, prazo_meses, status_contrato
FROM contratos;

-- Populando fato_pagamentos
INSERT INTO fato_pagamentos (pagamento_id, contrato_id, data_pagamento, valor_pago)
SELECT pagamento_id, contrato_id, data_pagamento, valor_pago
FROM pagamentos;
