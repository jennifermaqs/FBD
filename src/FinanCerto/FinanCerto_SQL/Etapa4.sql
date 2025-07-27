-- COMANDOS SQL DAS VIEWS 

-- Visão que retorna a soma de todos os valores do tipo entrada
-- Depois todos os valores do tipo saida
-- E por ultimo a diferença entre esses dois valores
CREATE OR REPLACE VIEW Resumo_Financeiro AS
SELECT
    u.ID_Usuario,
    u.Nome_Usuario,
    SUM(CASE WHEN c.Tipo_Categoria = 'Entrada' THEN t.Valor ELSE 0 END) AS Total_Entradas,
    SUM(CASE WHEN c.Tipo_Categoria = 'Saida' THEN t.Valor ELSE 0 END) AS Total_Saidas,
    SUM(CASE WHEN c.Tipo_Categoria = 'Entrada' THEN t.Valor ELSE 0 END) -
    SUM(CASE WHEN c.Tipo_Categoria = 'Saida' THEN t.Valor ELSE 0 END) AS Saldo
FROM Usuario u
LEFT JOIN Transacao t ON u.ID_Usuario = t.ID_Usuario
LEFT JOIN CategoriaTransacao c ON t.ID_Categoria = c.ID_Categoria
GROUP BY u.ID_Usuario, u.Nome_Usuario; 

-- Visão que retorna os produtos mais vendidos dos usuários
-- Where com o id do usuario retorna só os dele
CREATE OR REPLACE VIEW Produtos_Mais_Vendidos AS
SELECT
    u.ID_Usuario,
    u.Nome_Usuario,
    p.ID_Produto,
    p.Nome_Produto,
    SUM(vp.Quantidade) AS Total_Vendido
FROM Produto p
JOIN Venda_Produto vp ON p.ID_Produto = vp.ID_Produto
JOIN Usuario u ON p.ID_Usuario = u.ID_Usuario
GROUP BY u.ID_Usuario, u.Nome_Usuario, p.ID_Produto, p.Nome_Produto;

-- Visão que retorna o lucro dos produtos dos usuarios
CREATE OR REPLACE VIEW Lucro_Produtos AS
SELECT
    u.Nome_Usuario,
    u.ID_Usuario,
    p.ID_Produto,
    p.Nome_Produto,
    SUM(vp.Quantidade * (vp.Preco_Unitario_Venda - p.Preco_Custo)) AS Lucro_Total
FROM Produto p
JOIN Venda_Produto vp ON p.ID_Produto = vp.ID_Produto
JOIN Usuario u on u.ID_Usuario = p.ID_Usuario
GROUP BY p.ID_Produto, p.Nome_Produto, u.ID_Usuario, u.Nome_Usuario;

select * from Resumo_Financeiro r
ORDER BY r.ID_Usuario

SELECT * FROM Produtos_Mais_Vendidos pmv
ORDER BY total_vendido desc

SELECT * FROM Lucro_Produtos
where id_usuario = '1';

-- Criação de usuários e permissões 

-- criação usuário administrador 
CREATE ROLE usuario_admin WITH LOGIN PASSWORD '2025';

-- criação usuário de leitura
CREATE ROLE usuario_leitura WITH LOGIN PASSWORD '2520';

-- permissão de conexão ao banco pro usuario_admin
GRANT CONNECT ON DATABASE "FinanCerto" TO usuario_admin;

-- permissões pro usuario_admin ter privilégios totais de leitura e escrita para alterar todas as tabelas
GRANT USAGE ON SCHEMA public TO usuario_admin;


GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usuario_admin;

GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO usuario_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO usuario_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO usuario_admin;


-- permissão pra conectar ao banco
GRANT CONNECT ON DATABASE "FinanCerto" TO usuario_leitura;

-- permissões ao usuario_leitura de usar os schemas e realizar consultas
GRANT USAGE ON SCHEMA public TO usuario_leitura;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO usuario_leitura;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO usuario_leitura;
