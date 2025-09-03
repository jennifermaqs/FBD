-- Consulta 1: Resumo Financeiro do Usuário
-- Explicação: Mostra o total de entradas, saídas e o saldo de um usuário (ex: ID 1),
-- baseado no tipo da categoria. Transações sem categoria não entram no cálculo.
SELECT
    U.Nome_Usuario,
    SUM(CASE WHEN CT.Tipo_Categoria = 'Entrada' THEN T.Valor ELSE 0 END) AS Total_Entradas,
    SUM(CASE WHEN CT.Tipo_Categoria = 'Saida' THEN T.Valor ELSE 0 END) AS Total_Saidas,
    (SUM(CASE WHEN CT.Tipo_Categoria = 'Entrada' THEN T.Valor ELSE 0 END) - SUM(CASE WHEN CT.Tipo_Categoria = 'Saida' THEN T.Valor ELSE 0 END)) AS Saldo_Final
FROM Usuario U
JOIN Transacao T ON U.ID_Usuario = T.ID_Usuario
LEFT JOIN CategoriaTransacao CT ON T.ID_Categoria = CT.ID_Categoria
WHERE U.ID_Usuario = 1
GROUP BY U.Nome_Usuario;


-- Consulta 2: Gastos por Categoria
-- Explicação: Mostra quanto um usuário (ex: ID 1) gastou em cada categoria de saída.
SELECT
    CT.Nome_Categoria,
    SUM(T.Valor) AS Total_Gasto
FROM Transacao T
JOIN CategoriaTransacao CT ON T.ID_Categoria = CT.ID_Categoria
WHERE T.ID_Usuario = 1 AND CT.Tipo_Categoria = 'Saida'
GROUP BY CT.Nome_Categoria;


-- Consulta 3: Produtos Mais Vendidos
-- Explicação: Lista os produtos mais vendidos de um usuário (ex: ID 5) pela quantidade.
SELECT
    P.Nome_Produto,
    SUM(VP.Quantidade) AS Total_Vendido
FROM Venda_Produto VP
JOIN Produto P ON VP.ID_Produto = P.ID_Produto
JOIN Venda V ON VP.ID_Venda = V.ID_Venda
WHERE V.ID_Usuario = 5
GROUP BY P.Nome_Produto
ORDER BY Total_Vendido DESC;


-- Consulta 4: Lucro por Produto
-- Explicação: Calcula o lucro total para cada produto vendido por um usuário (ex: ID 1),
-- usando o preço exato da venda para maior precisão.
SELECT
    P.Nome_Produto,
    SUM(VP.Quantidade) AS Unidades_Vendidas,
    SUM(VP.Quantidade * (VP.Preco_Unitario_Venda - P.Preco_Custo)) AS Lucro_Total
FROM Venda_Produto VP
JOIN Produto P ON VP.ID_Produto = P.ID_Produto
JOIN Venda V ON VP.ID_Venda = V.ID_Venda
WHERE V.ID_Usuario = 1
GROUP BY P.Nome_Produto;


-- Consulta 5: Vendas por Método de Pagamento
-- Explicação: Mostra o total vendido para cada forma de pagamento de um usuário (ex: ID 5).
SELECT
    Metodo_Pagamento,
    SUM(Valor_Total_Venda) AS Valor_Total
FROM Venda
WHERE ID_Usuario = 5
GROUP BY Metodo_Pagamento;


-- Consulta 6: Extrato de Transações do Usuário
-- Explicação: Lista todas as transações de um usuário (ex: ID 3) com sua categoria.
SELECT
    T.Data_Transacao,
    T.Descricao,
    T.Valor,
    COALESCE(CT.Nome_Categoria, 'Sem Categoria') AS Categoria
FROM Transacao T
LEFT JOIN CategoriaTransacao CT ON T.ID_Categoria = CT.ID_Categoria
WHERE T.ID_Usuario = 3
ORDER BY T.Data_Transacao DESC;


-- Consulta 7: Detalhes de uma Venda
-- Explicação: Mostra todos os produtos de uma venda específica (ex: ID 9).
SELECT
    V.ID_Venda,
    V.Data_Venda,
    P.Nome_Produto,
    VP.Quantidade,
    VP.Preco_Unitario_Venda,
    (VP.Quantidade * VP.Preco_Unitario_Venda) AS Subtotal
FROM Venda V
JOIN Venda_Produto VP ON V.ID_Venda = VP.ID_Venda
JOIN Produto P ON VP.ID_Produto = P.ID_Produto
WHERE V.ID_Venda = 9;
