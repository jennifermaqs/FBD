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
class TransacaoBase(BaseModel):
    data_transacao: date
    descricao: Optional[str] = None
    valor: Decimal

class TransacaoCreate(TransacaoBase):
    id_usuario: int
    id_categoria: int

class TransacaoUpdate(BaseModel):
    data_transacao: Optional[date] = None
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    id_categoria: Optional[int] = None

class TransacaoResponse(TransacaoBase):
    id_transacao: int
    id_usuario: int
    id_categoria: int

# Router
router = APIRouter(prefix="/transacoes", tags=["Transações"])

# CRUD para Transações
@router.post("/", response_model=TransacaoResponse)
async def criar_transacao(transacao: TransacaoCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    # Verificar se categoria existe
    cur.execute("SELECT id_categoria FROM categoriatransacao WHERE id_categoria = %s", (transacao.id_categoria,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Categoria não encontrada")
    
    try:
        cur.execute(
            """INSERT INTO transacao (data_transacao, descricao, valor, id_usuario, id_categoria) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id_transacao""",
            (transacao.data_transacao, transacao.descricao, transacao.valor, 
             transacao.id_usuario, transacao.id_categoria)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return TransacaoResponse(
            id_transacao=result[0],
            data_transacao=transacao.data_transacao,
            descricao=transacao.descricao,
            valor=transacao.valor,
            id_usuario=transacao.id_usuario,
            id_categoria=transacao.id_categoria
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar transação: {e}")

@router.get("/usuario/{usuario_id}", response_model=List[TransacaoResponse])
async def listar_transacoes_usuario(usuario_id: int, skip: int = 0, limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT id_transacao, data_transacao, descricao, valor, id_usuario, id_categoria 
           FROM transacao WHERE id_usuario = %s ORDER BY data_transacao DESC OFFSET %s LIMIT %s""",
        (usuario_id, skip, limit)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [TransacaoResponse(
        id_transacao=t[0], data_transacao=t[1], descricao=t[2], 
        valor=t[3], id_usuario=t[4], id_categoria=t[5]
    ) for t in rows]

@router.get("/{transacao_id}", response_model=TransacaoResponse)
async def obter_transacao(transacao_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_transacao, data_transacao, descricao, valor, id_usuario, id_categoria FROM transacao WHERE id_transacao = %s", (transacao_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return TransacaoResponse(
            id_transacao=row[0], data_transacao=row[1], descricao=row[2],
            valor=row[3], id_usuario=row[4], id_categoria=row[5]
        )
    raise HTTPException(404, "Transação não encontrada")

@router.patch("/{transacao_id}")
async def atualizar_transacao_parcial(transacao_id: int, transacao: TransacaoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_transacao FROM transacao WHERE id_transacao = %s", (transacao_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Transação não encontrada")
    
    fields = []
    values = []
    for campo, valor in transacao.dict(exclude_unset=True).items():
        # Verificar se categoria existe quando atualizar categoria
        if campo == "id_categoria":
            cur.execute("SELECT id_categoria FROM categoriatransacao WHERE id_categoria = %s", (valor,))
            if not cur.fetchone():
                cur.close()
                conn.close()
                raise HTTPException(404, "Categoria não encontrada")
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(transacao_id)
    try:
        cur.execute(f"UPDATE transacao SET {', '.join(fields)} WHERE id_transacao=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Transação atualizada"}

@router.delete("/{transacao_id}")
async def deletar_transacao(transacao_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transacao WHERE id_transacao=%s", (transacao_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Transação removida"}
