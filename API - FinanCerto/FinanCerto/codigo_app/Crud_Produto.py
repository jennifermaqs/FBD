from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
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

# Modelos Pydantic
class ProdutoBase(BaseModel):
    nome_produto: str
    preco_custo: Decimal
    preco_venda: Decimal

class ProdutoCreate(ProdutoBase):
    id_usuario: int

class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None
    preco_custo: Optional[Decimal] = None
    preco_venda: Optional[Decimal] = None

class ProdutoResponse(ProdutoBase):
    id_produto: int
    id_usuario: int

# Router
router = APIRouter(prefix="/produtos", tags=["Produtos"])

# CRUD para Produtos
@router.post("/", response_model=ProdutoResponse)
async def criar_produto(produto: ProdutoCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            """INSERT INTO produto (nome_produto, preco_custo, preco_venda, id_usuario) 
               VALUES (%s, %s, %s, %s) RETURNING id_produto""",
            (produto.nome_produto, produto.preco_custo, produto.preco_venda, produto.id_usuario)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return ProdutoResponse(
            id_produto=result[0],
            nome_produto=produto.nome_produto,
            preco_custo=produto.preco_custo,
            preco_venda=produto.preco_venda,
            id_usuario=produto.id_usuario
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar produto: {e}")

@router.get("/usuario/{usuario_id}", response_model=List[ProdutoResponse])
async def listar_produtos_usuario(usuario_id: int, skip: int = 0, limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT id_produto, nome_produto, preco_custo, preco_venda, id_usuario 
           FROM produto WHERE id_usuario = %s OFFSET %s LIMIT %s""",
        (usuario_id, skip, limit)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [ProdutoResponse(
        id_produto=p[0], nome_produto=p[1], preco_custo=p[2], 
        preco_venda=p[3], id_usuario=p[4]
    ) for p in rows]

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_produto, nome_produto, preco_custo, preco_venda, id_usuario FROM produto WHERE id_produto = %s", (produto_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return ProdutoResponse(
            id_produto=row[0], nome_produto=row[1], preco_custo=row[2],
            preco_venda=row[3], id_usuario=row[4]
        )
    raise HTTPException(404, "Produto não encontrado")

@router.patch("/{produto_id}")
async def atualizar_produto_parcial(produto_id: int, produto: ProdutoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_produto FROM produto WHERE id_produto = %s", (produto_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Produto não encontrado")
    
    fields = []
    values = []
    for campo, valor in produto.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(produto_id)
    try:
        cur.execute(f"UPDATE produto SET {', '.join(fields)} WHERE id_produto=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Produto atualizado"}

@router.delete("/{produto_id}")
async def deletar_produto(produto_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM produto WHERE id_produto=%s", (produto_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Produto removido"}
