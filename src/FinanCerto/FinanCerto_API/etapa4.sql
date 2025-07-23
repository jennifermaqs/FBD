-- Visão 1: Detalhes de uma Venda
-- Explicação: Mostra todos os produtos de uma venda específica (ex: ID 9).
CREATE OR REPLACE VIEW admin_detalhes_venda AS
SELECT
    V.ID_Venda,
    V.Data_Venda,
    P.Nome_Produto,
    VP.Quantidade,
    VP.Preco_Unitario_Venda,
    (VP.Quantidade * VP.Preco_Unitario_Venda) AS Subtotal
FROM Venda V
JOIN Venda_Produto VP ON V.ID_Venda = VP.ID_Venda
JOIN Produto P ON VP.ID_Produto = P.ID_Produto;

---

-- Visão 2: Produtos Mais Vendidos (Admin)
-- Explicação: Lista os produtos mais vendidos por subtotal, fornecendo detalhes de preço e quantidade.

CREATE OR REPLACE VIEW admin_produtos_mais_vendidos AS
SELECT
    P.Nome_Produto,
    SUM(VP.Quantidade) AS Total_Quantidade_Vendida,
    SUM(VP.Quantidade * VP.Preco_Unitario_Venda) AS Total_Subtotal_Vendido
FROM Venda_Produto VP
JOIN Produto P ON VP.ID_Produto = P.ID_Produto
GROUP BY P.Nome_Produto
ORDER BY Total_Subtotal_Vendido DESC;

-- Visão 3: Resumo Financeiro do Usuário
-- Explicação: Mostra o total de entradas, saídas e o saldo de um usuário (ex: ID 1),
-- baseado no tipo da categoria. Transações sem categoria não entram no cálculo.
CREATE OR REPLACE VIEW usuario_resumo_financeiro AS
SELECT
    U.ID_Usuario, 
    U.Nome_Usuario,
    SUM(CASE WHEN CT.Tipo_Categoria = 'Entrada' THEN T.Valor ELSE 0 END) AS Total_Entradas,
    SUM(CASE WHEN CT.Tipo_Categoria = 'Saida' THEN T.Valor ELSE 0 END) AS Total_Saidas,
    (SUM(CASE WHEN CT.Tipo_Categoria = 'Entrada' THEN T.Valor ELSE 0 END) - SUM(CASE WHEN CT.Tipo_Categoria = 'Saida' THEN T.Valor ELSE 0 END)) AS Saldo_Final
FROM Usuario U
JOIN Transacao T ON U.ID_Usuario = T.ID_Usuario
LEFT JOIN CategoriaTransacao CT ON T.ID_Categoria = CT.ID_Categoria
GROUP BY U.ID_Usuario, U.Nome_Usuario;

---

-- Visão 4: Produtos Mais Vendidos (Usuário)
-- Explicação: Lista os produtos mais vendidos de um usuário (ex: ID 9) pela quantidade.
CREATE OR REPLACE VIEW usuario_produtos_mais_vendidos AS
SELECT
    P.Nome_Produto,
    SUM(VP.Quantidade) AS Total_Vendido
FROM Venda_Produto VP
JOIN Produto P ON VP.ID_Produto = P.ID_Produto
JOIN Venda V ON VP.ID_Venda = V.ID_Venda
GROUP BY P.Nome_Produto
ORDER BY Total_Vendido DESC;


-- Habilitar RLS nas tabelas relevantes
ALTER TABLE Transacao ENABLE ROW LEVEL SECURITY;
ALTER TABLE Venda ENABLE ROW LEVEL SECURITY;

-- Criar políticas de RLS para o usuario_leitura
-- (Assumindo que o Nome_Usuario na sua tabela 'Usuario' corresponda ao nome do usuário do banco de dados)
CREATE POLICY polit_transacao_usuario ON Transacao
FOR SELECT
TO usuario_leitura
USING (ID_Usuario = (SELECT ID_Usuario FROM Usuario WHERE Nome_Usuario = current_user));

CREATE POLICY polit_venda_usuario ON Venda
FOR SELECT
TO usuario_leitura
USING (ID_Usuario = (SELECT ID_Usuario FROM Usuario WHERE Nome_Usuario = current_user));

-- Para o usuario_admin
GRANT ALL PRIVILEGES ON admin_detalhes_venda TO usuario_admin;
GRANT ALL PRIVILEGES ON admin_produtos_mais_vendidos TO usuario_admin;
GRANT ALL PRIVILEGES ON usuario_resumo_financeiro TO usuario_admin;
GRANT ALL PRIVILEGES ON usuario_produtos_mais_vendidos TO usuario_admin;

-- Para o usuario_leitura (apenas SELECT nas visões de usuário)
GRANT SELECT ON usuario_resumo_financeiro TO usuario_leitura;
GRANT SELECT ON usuario_produtos_mais_vendidos TO usuario_leitura;

SELECT * FROM admin_detalhes_venda LIMIT 10;
SELECT * FROM admin_produtos_mais_vendidos LIMIT 10;

SELECT * FROM usuario_resumo_financeiro LIMIT 10;
SELECT * FROM usuario_produtos_mais_vendidos LIMIT 10;