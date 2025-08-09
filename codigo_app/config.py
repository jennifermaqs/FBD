# Configuração centralizada do banco de dados
# Para alterar a configuração do banco, modifique apenas este arquivo

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/ProjetoFBD"

# Parâmetros de conexão separados (caso precise usar individualmente)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ProjetoFBD",
    "user": "postgres",
    "password": "1234"
}
