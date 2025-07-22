INSERT INTO Usuario (Nome_Usuario, Email, Senha) VALUES
('Ana Silva', 'ana.silva@email.com', 'senha123'),
('Bruno Costa', 'bruno.costa@email.com', 'senha123'),
('Carla Dias', 'carla.dias@email.com', 'senha123'),
('Daniel Martins', 'daniel.martins@email.com', 'senha123'),
('Eduarda Lima', 'eduarda.lima@email.com', 'senha123'),
('Fábio Pereira', 'fabio.pereira@email.com', 'senha123'),
('Gabriela Souza', 'gabriela.souza@email.com', 'senha123'),
('Heitor Alves', 'heitor.alves@email.com', 'senha123'),
('Isabela Rocha', 'isabela.rocha@email.com', 'senha123'),
('João Mendes', 'joao.mendes@email.com', 'senha123');

-- Inserindo Detalhes para os Usuários
INSERT INTO DetalhesUsuario (ID_Usuario, Data_Nascimento, Telefone_Contato, CPF, Nome_Negocio) VALUES
(1, '1990-05-15', '(11) 98765-4321', '111.222.333-44', 'Ana Doces'),
(2, '1988-11-20', '(21) 91234-5678', '222.333.444-55', 'Bruno Artesanato'),
(3, '1995-02-10', '(31) 95555-4444', '333.444.555-66', 'Carla Consultoria'),
(4, '1992-08-30', '(41) 98888-7777', '444.555.666-77', 'Dani Entregas'),
(5, '1998-07-25', '(51) 97777-6666', '555.666.777-88', 'Duda Modas'),
(6, '1985-03-12', '(61) 96666-5555', '666.777.888-99', 'Fábio Reparos'),
(7, '1993-09-05', '(71) 95555-1111', '777.888.999-00', 'Gabi Design'),
(8, '1991-12-01', '(81) 94444-2222', '888.999.000-11', 'Heitor Gráfica'),
(9, '1997-06-18', '(91) 93333-8888', '999.000.111-22', 'Bela Bijoux'),
(10, '1989-10-22', '(19) 92222-3333', '000.111.222-33', 'J Mendes Serviços');

-- Inserindo Categorias de Transação
INSERT INTO CategoriaTransacao (Nome_Categoria, Tipo_Categoria, ID_Usuario) VALUES
('Receita de Vendas', 'Entrada', 1),
('Aluguel', 'Saida', 1),
('Fornecedores', 'Saida', 1),
('Salário', 'Entrada', 2),
('Marketing', 'Saida', 2),
('Contas de Consumo (Água, Luz)', 'Saida', 3),
('Venda de Serviços', 'Entrada', 3),
('Transporte', 'Saida', 4),
('Venda de Produtos', 'Entrada', 5),
('Impostos', 'Saida', 5),
('Contas de Consumo', 'Saida', 1); -- Categoria adicionada para corrigir dados

-- Inserindo Transações
INSERT INTO Transacao (Data_Transacao, Descricao, Valor, ID_Usuario, ID_Categoria) VALUES
('2024-05-01', 'Pagamento fornecedor de farinha', 150.00, 1, 3),
('2024-05-02', 'Venda de bolo de chocolate', 50.00, 1, 1),
('2024-05-03', 'Pagamento da conta de luz', 120.50, 1, 11), -- FK corrigida para 11
('2024-05-05', 'Recebimento por consultoria', 500.00, 3, 7),
('2024-05-06', 'Compra de material de escritório', 75.25, 3, NULL),
('2024-05-07', 'Venda de blusa', 89.90, 5, 9),
('2024-05-08', 'Pagamento de anúncio online', 200.00, 2, 5),
('2024-05-09', 'Recebimento por serviço de entrega', 45.00, 4, NULL),
('2024-05-10', 'Pagamento aluguel do espaço', 800.00, 1, 2),
('2024-05-11', 'Venda de artesanato', 120.00, 2, 4);

-- Inserindo Produtos
INSERT INTO Produto (Nome_Produto, Preco_Custo, Preco_Venda, ID_Usuario) VALUES
('Bolo de Pote', 5.00, 10.00, 1),
('Brigadeiro (unidade)', 1.50, 3.00, 1),
('Caixa de Madeira Decorada', 15.00, 35.00, 2),
('Colar de Miçangas', 8.00, 20.00, 9),
('Camiseta Estampada', 25.00, 59.90, 5),
('Calça Jeans', 50.00, 119.90, 5),
('Caneca Personalizada', 12.00, 25.00, 8),
('Cartão de Visita (cento)', 20.00, 45.00, 8),
('Hora de Consultoria', 50.00, 150.00, 3),
('Formatação de PC', 40.00, 100.00, 6);

-- Inserindo Vendas
INSERT INTO Venda (Data_Venda, Valor_Total_Venda, Metodo_Pagamento, ID_Usuario) VALUES
('2024-05-15', 40.00, 'Pix', 1),
('2024-05-15', 35.00, 'Dinheiro', 2),
('2024-05-16', 119.90, 'Cartão de Crédito', 5),
('2024-05-17', 90.00, 'Cartão de Débito', 8),
('2024-05-18', 20.00, 'Pix', 9),
('2024-05-19', 150.00, 'Transferência', 3),
('2024-05-20', 100.00, 'Dinheiro', 6),
('2024-05-21', 59.90, 'Cartão de Crédito', 5),
('2024-05-22', 16.00, 'Pix', 1),
('2024-05-23', 45.00, 'Cartão de Débito', 8);

-- Inserindo Itens da Venda (Venda_Produto)
INSERT INTO Venda_Produto (ID_Venda, ID_Produto, Quantidade, Preco_Unitario_Venda) VALUES
(1, 1, 4, 10.00),
(2, 3, 1, 35.00),
(3, 6, 1, 119.90),
(4, 8, 2, 45.00),
(5, 4, 1, 20.00),
(6, 9, 1, 150.00),
(7, 10, 1, 100.00),
(8, 5, 1, 59.90),
(9, 1, 1, 10.00),
(9, 2, 2, 3.00),
(10, 7, 1, 25.00);