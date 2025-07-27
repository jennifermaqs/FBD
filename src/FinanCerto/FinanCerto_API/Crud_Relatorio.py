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
    
    # Calcular total de entradas
    cur.execute(
        """SELECT COALESCE(SUM(t.valor), 0) as total_entradas 
           FROM transacao t 
           JOIN categoriatransacao c ON t.id_categoria = c.id_categoria 
           WHERE t.id_usuario = %s AND c.tipo_categoria = 'Entrada'""",
        (usuario_id,)
    )
    entradas = cur.fetchone()[0]
    
    # Calcular total de saídas
    cur.execute(
        """SELECT COALESCE(SUM(t.valor), 0) as total_saidas 
           FROM transacao t 
           JOIN categoriatransacao c ON t.id_categoria = c.id_categoria 
           WHERE t.id_usuario = %s AND c.tipo_categoria = 'Saida'""",
        (usuario_id,)
    )
    saidas = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    saldo = float(entradas) - float(saidas)
    
    return {
        "usuario_id": usuario_id,
        "total_entradas": float(entradas),
        "total_saidas": float(saidas),
        "saldo_atual": saldo
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
    
    # Calcular lucro das vendas (preço venda - preço custo)
    cur.execute(
        """SELECT COALESCE(SUM(vp.quantidade * (vp.preco_unitario_venda - p.preco_custo)), 0) as lucro_vendas
           FROM venda_produto vp
           JOIN produto p ON vp.id_produto = p.id_produto
           JOIN venda v ON vp.id_venda = v.id_venda
           WHERE v.id_usuario = %s""",
        (usuario_id,)
    )
    lucro_vendas = cur.fetchone()[0]
    
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
    
    cur.execute(
        """SELECT p.nome_produto, SUM(vp.quantidade) as total_vendido, 
                  SUM(vp.quantidade * vp.preco_unitario_venda) as receita_total
           FROM venda_produto vp
           JOIN produto p ON vp.id_produto = p.id_produto
           JOIN venda v ON vp.id_venda = v.id_venda
           WHERE v.id_usuario = %s
           GROUP BY p.id_produto, p.nome_produto
           ORDER BY total_vendido DESC
           LIMIT %s""",
        (usuario_id, limit)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {
            "nome_produto": row[0],
            "total_vendido": row[1],
            "receita_total": float(row[2])
        }
        for row in rows
    ]
