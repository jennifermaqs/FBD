from fastapi import HTTPException, APIRouter
import psycopg2
from config import DATABASE_URL

def get_connection():
    """Função para obter conexão com o banco de dados"""
    try:
        # Extrair parâmetros da URL de conexão
        url_parts = DATABASE_URL.replace("postgresql://", "").split("@")
        user_pass = url_parts[0].split(":")
        host_db = url_parts[1].split("/")
        host_port = host_db[0].split(":")
        
        conn = psycopg2.connect(
            host=host_port[0],
            port=int(host_port[1]) if len(host_port) > 1 else 5432,
            database=host_db[1],
            user=user_pass[0],
            password=user_pass[1]
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na conexão com o banco: {str(e)}")

# Router
router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

# Relatórios e estatísticas
@router.get("/saldo/{usuario_id}")
async def obter_saldo_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # Usar a view Resumo_Financeiro
    cur.execute(
        """SELECT id_usuario, nome_usuario, total_entradas, total_saidas, saldo 
           FROM resumo_financeiro 
           WHERE id_usuario = %s""",
        (usuario_id,)
    )
    result = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "usuario_id": result[0],
        "nome_usuario": result[1],
        "total_entradas": float(result[2]),
        "total_saidas": float(result[3]),
        "saldo_atual": float(result[4])
    }

@router.get("/vendas/{usuario_id}")
async def relatorio_vendas_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT COUNT(*) as total_vendas, COALESCE(SUM(valor_total_venda), 0) as valor_total 
           FROM venda WHERE id_usuario = %s""",
        (usuario_id,)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return {
        "usuario_id": usuario_id,
        "total_vendas": result[0],
        "valor_total_vendas": float(result[1])
    }

@router.get("/lucro/{usuario_id}")
async def relatorio_lucro_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    # Usar a view Lucro_Produtos
    cur.execute(
        """SELECT SUM(lucro_total) as lucro_total_vendas
           FROM lucro_produtos 
           WHERE id_usuario = %s""",
        (usuario_id,)
    )
    result = cur.fetchone()
    lucro_vendas = result[0] if result[0] is not None else 0
    
    cur.close()
    conn.close()
    
    return {
        "usuario_id": usuario_id,
        "lucro_total_vendas": float(lucro_vendas)
    }

@router.get("/produtos-mais-vendidos/{usuario_id}")
async def produtos_mais_vendidos(usuario_id: int, limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    
    # Usar a view Produtos_Mais_Vendidos
    cur.execute(
        """SELECT id_produto, nome_produto, total_vendido
           FROM produtos_mais_vendidos
           WHERE id_usuario = %s
           ORDER BY total_vendido DESC
           LIMIT %s""",
        (usuario_id, limit)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {
            "id_produto": row[0],
            "nome_produto": row[1],
            "total_vendido": row[2]
        }
        for row in rows
    ]
