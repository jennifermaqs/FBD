CREATE TABLE Endereco (
    id_endereco INT PRIMARY KEY,
    rua VARCHAR(80) NOT NULL,
    numero VARCHAR(10) NOT NULL,
	bairro VARCHAR(40) NOT NULL,
	cidade VARCHAR(60) NOT NULL
);

CREATE TABLE Restaurante (
id_restaurante INT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
data_fundacao DATE NOT NULL,
tipo_cozinha VARCHAR(40) NOT NULL,
selo_sustentabilidade BOOLEAN NOT NULL,
id_endereco INT,
CONSTRAINT FK_Restaurante_Endereco
	FOREIGN KEY (id_endereco)
	REFERENCES Endereco(id_endereco)

);

CREATE TABLE Ingrediente (
id_ingrediente INT PRIMARY KEY,
nome VARCHAR(80) NOT NULL,
tipo VARCHAR(30) NOT NULL,
origem VARCHAR(50) NOT NULL,
organico BOOLEAN NOT NULL,
fornecedor VARCHAR(100) NOT NULL,
quantidade_estoque NUMERIC(8,2) NOT NULL,
unidade_medida VARCHAR(10) NOT NULL,
validade DATE NOT NULL
);

CREATE TABLE Funcionario (
id_funcionario INT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
cargo VARCHAR(40) NOT NULL,
data_admissao DATE NOT NULL,
cpf VARCHAR(11) UNIQUE NOT NULL,
email VARCHAR(80) UNIQUE NOT NULL,
data_nascimento DATE NOT NULL,
salario NUMERIC(10,2) NOT NULL,
id_restaurante INT NOT NULL,
	CONSTRAINT FK_Funcionario_Restaurante
		FOREIGN KEY (id_restaurante)
		REFERENCES Restaurante(id_restaurante)
);

CREATE TABLE Cardapio (
id_cardapio INT PRIMARY KEY,
nome VARCHAR(80) NOT NULL,
descricao VARCHAR(200) NOT NULL,
data_inicio DATE NOT NULL,
data_fim DATE NULL,
publico_alvo VARCHAR(50) NOT NULL,
eh_vegano BOOLEAN NOT NULL,
id_restaurante INT NOT NULL, 
	CONSTRAINT FK_Cardapio_Restaurante
		FOREIGN KEY (id_restaurante)
		REFERENCES Restaurante(id_restaurante)
);


CREATE TABLE Receita (
id_receita INT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
descricao VARCHAR(200) NOT NULL,
tempo_preparo INT NOT NULL,
dificuldade VARCHAR(20) NOT NULL,
eh_saudavel BOOLEAN NOT NULL,
quantidade_porcoes INT NOT NULL,
id_cardapio INT NOT NULL,
	CONSTRAINT FK_Receita_Cardapio
		FOREIGN KEY (id_cardapio)
		REFERENCES Cardapio(id_cardapio)
);


CREATE TABLE TelefoneRestaurante (
id_telefone INT PRIMARY KEY,
numero VARCHAR(15) NOT NULL,
id_restaurante INT NOT NULL,
	CONSTRAINT FK_TelefoneRestaurante_Restaurante
		FOREIGN KEY (id_restaurante)
		REFERENCES Restaurante(id_restaurante)
);

CREATE TABLE ReceitaIngrediente (
id_receita INT NOT NULL,
id_ingrediente INT NOT NULL,
quantidade_utilizada NUMERIC(8,2) NOT NULL,
unidade_medida VARCHAR(10) NOT NULL,

	PRIMARY KEY(id_receita, id_ingrediente),

	CONSTRAINT FK_ReceitaIngrediente_Receita
		FOREIGN KEY (id_receita)
		REFERENCES Receita(id_receita),
		
	CONSTRAINT FK_ReceitaIngrediente_Ingrediente
		FOREIGN KEY (id_ingrediente)
		REFERENCES Ingrediente(id_ingrediente)

);

CREATE TABLE GerenteRestaurante (
id_restaurante INT PRIMARY KEY,
id_funcionario INT UNIQUE NOT NULL,

	CONSTRAINT FK_Gerente_Restaurante
		FOREIGN KEY (id_restaurante)
		REFERENCES Restaurante(id_restaurante),

	CONSTRAINT FK_Gerente_Funcionario
		FOREIGN KEY (id_funcionario)
		REFERENCES Funcionario(id_funcionario)
);