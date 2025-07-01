-- usuários do sistema.
CREATE TABLE Usuario (
    ID_Usuario SERIAL PRIMARY KEY,
    Nome_Usuario VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Senha VARCHAR(255) NOT NULL
);

-- detalhes do usuário 
CREATE TABLE DetalhesUsuario (
    ID_Usuario INT PRIMARY KEY,
    Data_Nascimento DATE,
    Telefone_Contato VARCHAR(20),
    CPF VARCHAR(14) UNIQUE,
    Nome_Negocio VARCHAR(100),
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

-- Tabela para categorizar as transações 
CREATE TABLE CategoriaTransacao (
    ID_Categoria SERIAL PRIMARY KEY,
    Nome_Categoria VARCHAR(100) NOT NULL,
    Tipo_Categoria VARCHAR(7) CHECK (Tipo_Categoria IN ('Entrada', 'Saida')),
    ID_Usuario INT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

-- Tabela que registra as entradas e saídas de dinheiro
CREATE TABLE Transacao (
    ID_Transacao SERIAL PRIMARY KEY,
    Data_Transacao DATE NOT NULL,
    Descricao VARCHAR(255),
    Valor DECIMAL(10, 2) NOT NULL,
    ID_Usuario INT,
    ID_Categoria INT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario),
    FOREIGN KEY (ID_Categoria) REFERENCES CategoriaTransacao(ID_Categoria)
);

-- Tabela para guardar os produtos à venda
CREATE TABLE Produto (
    ID_Produto SERIAL PRIMARY KEY,
    Nome_Produto VARCHAR(100) NOT NULL,
    Preco_Custo DECIMAL(10, 2) NOT NULL,
    Preco_Venda DECIMAL(10, 2) NOT NULL,
    ID_Usuario INT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

-- Tabela que registra uma venda
CREATE TABLE Venda (
    ID_Venda SERIAL PRIMARY KEY,
    Data_Venda DATE NOT NULL,
    Valor_Total_Venda DECIMAL(10, 2) NOT NULL,
    Metodo_Pagamento VARCHAR(50),
    ID_Usuario INT,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario)
);

-- Tabela que liga os produtos a uma venda .
CREATE TABLE Venda_Produto (
    ID_Venda INT,
    ID_Produto INT,
    Quantidade INT NOT NULL,
    Preco_Unitario_Venda DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (ID_Venda, ID_Produto),
    FOREIGN KEY (ID_Venda) REFERENCES Venda(ID_Venda),
    FOREIGN KEY (ID_Produto) REFERENCES Produto(ID_Produto)
);


