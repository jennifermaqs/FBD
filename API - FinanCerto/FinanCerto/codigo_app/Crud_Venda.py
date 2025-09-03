from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
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
class VendaProdutoBase(BaseModel):
    id_produto: int
    quantidade: int
    preco_unitario_venda: Decimal

class VendaBase(BaseModel):
    data_venda: date
    valor_total_venda: Decimal
    metodo_pagamento: Optional[str] = None

class VendaCreate(VendaBase):
    id_usuario: int
    produtos: List[VendaProdutoBase]

class VendaUpdate(BaseModel):
    data_venda: Optional[date] = None
    valor_total_venda: Optional[Decimal] = None
    metodo_pagamento: Optional[str] = None

class VendaResponse(VendaBase):
    id_venda: int
    id_usuario: int

class VendaProdutoResponse(VendaProdutoBase):
    id_venda: int

# Router
router = APIRouter(prefix="/vendas", tags=["Vendas"])

# CRUD para Vendas
@router.post("/", response_model=VendaResponse)
async def criar_venda(venda: VendaCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Iniciar transação
        cur.execute("BEGIN")
        
        # Criar a venda
        cur.execute(
            """INSERT INTO venda (data_venda, valor_total_venda, metodo_pagamento, id_usuario) 
               VALUES (%s, %s, %s, %s) RETURNING id_venda""",
            (venda.data_venda, venda.valor_total_venda, venda.metodo_pagamento, venda.id_usuario)
        )
        venda_result = cur.fetchone()
        id_venda = venda_result[0]
        
        # Adicionar produtos à venda
        for produto_venda in venda.produtos:
            cur.execute(
                """INSERT INTO venda_produto (id_venda, id_produto, quantidade, preco_unitario_venda) 
                   VALUES (%s, %s, %s, %s)""",
                (id_venda, produto_venda.id_produto, produto_venda.quantidade, produto_venda.preco_unitario_venda)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return VendaResponse(
            id_venda=id_venda,
            data_venda=venda.data_venda,
            valor_total_venda=venda.valor_total_venda,
            metodo_pagamento=venda.metodo_pagamento,
            id_usuario=venda.id_usuario
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar venda: {e}")

@router.get("/usuario/{usuario_id}", response_model=List[VendaResponse])
async def listar_vendas_usuario(usuario_id: int, skip: int = 0, limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT id_venda, data_venda, valor_total_venda, metodo_pagamento, id_usuario 
           FROM venda WHERE id_usuario = %s ORDER BY data_venda DESC OFFSET %s LIMIT %s""",
        (usuario_id, skip, limit)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [VendaResponse(
        id_venda=v[0], data_venda=v[1], valor_total_venda=v[2],
        metodo_pagamento=v[3], id_usuario=v[4]
    ) for v in rows]

@router.get("/{venda_id}", response_model=VendaResponse)
async def obter_venda(venda_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_venda, data_venda, valor_total_venda, metodo_pagamento, id_usuario FROM venda WHERE id_venda = %s", (venda_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return VendaResponse(
            id_venda=row[0], data_venda=row[1], valor_total_venda=row[2],
            metodo_pagamento=row[3], id_usuario=row[4]
        )
    raise HTTPException(404, "Venda não encontrada")

@router.get("/{venda_id}/produtos", response_model=List[VendaProdutoResponse])
async def listar_produtos_venda(venda_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_venda, id_produto, quantidade, preco_unitario_venda FROM venda_produto WHERE id_venda = %s", (venda_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [VendaProdutoResponse(
        id_venda=vp[0], id_produto=vp[1], quantidade=vp[2], preco_unitario_venda=vp[3]
    ) for vp in rows]

@router.patch("/{venda_id}")
async def atualizar_venda_parcial(venda_id: int, venda: VendaUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_venda FROM venda WHERE id_venda = %s", (venda_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Venda não encontrada")
    
    fields = []
    values = []
    for campo, valor in venda.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(venda_id)
    try:
        cur.execute(f"UPDATE venda SET {', '.join(fields)} WHERE id_venda=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Venda atualizada"}

@router.delete("/{venda_id}")
async def deletar_venda(venda_id: int):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Iniciar transação
        cur.execute("BEGIN")
        
        # Deletar produtos da venda primeiro
        cur.execute("DELETE FROM venda_produto WHERE id_venda=%s", (venda_id,))
        
        # Deletar a venda
        cur.execute("DELETE FROM venda WHERE id_venda=%s", (venda_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        return {"msg": "Venda removida"}
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao deletar venda: {e}")
