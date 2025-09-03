from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
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
class CategoriaTransacaoBase(BaseModel):
    nome_categoria: str
    tipo_categoria: str  # 'Entrada' ou 'Saida'

class CategoriaTransacaoCreate(CategoriaTransacaoBase):
    id_usuario: int

class CategoriaTransacaoUpdate(BaseModel):
    nome_categoria: Optional[str] = None
    tipo_categoria: Optional[str] = None

class CategoriaTransacaoResponse(CategoriaTransacaoBase):
    id_categoria: int
    id_usuario: int

# Router
router = APIRouter(prefix="/categorias", tags=["Categorias"])

# CRUD para Categorias de Transação
@router.post("/", response_model=CategoriaTransacaoResponse)
async def criar_categoria(categoria: CategoriaTransacaoCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    if categoria.tipo_categoria not in ['Entrada', 'Saida']:
        cur.close()
        conn.close()
        raise HTTPException(400, "Tipo de categoria deve ser 'Entrada' ou 'Saida'")
    
    try:
        cur.execute("INSERT INTO categoriatransacao (nome_categoria, tipo_categoria, id_usuario) VALUES (%s, %s, %s) RETURNING id_categoria",
                   (categoria.nome_categoria, categoria.tipo_categoria, categoria.id_usuario))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return CategoriaTransacaoResponse(
            id_categoria=result[0],
            nome_categoria=categoria.nome_categoria,
            tipo_categoria=categoria.tipo_categoria,
            id_usuario=categoria.id_usuario
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar categoria: {e}")

@router.get("/usuario/{usuario_id}", response_model=List[CategoriaTransacaoResponse])
async def listar_categorias_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria, nome_categoria, tipo_categoria, id_usuario FROM categoriatransacao WHERE id_usuario = %s", (usuario_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [CategoriaTransacaoResponse(id_categoria=c[0], nome_categoria=c[1], tipo_categoria=c[2], id_usuario=c[3]) for c in rows]

@router.get("/{categoria_id}", response_model=CategoriaTransacaoResponse)
async def obter_categoria(categoria_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria, nome_categoria, tipo_categoria, id_usuario FROM categoriatransacao WHERE id_categoria = %s", (categoria_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return CategoriaTransacaoResponse(id_categoria=row[0], nome_categoria=row[1], tipo_categoria=row[2], id_usuario=row[3])
    raise HTTPException(404, "Categoria não encontrada")

@router.patch("/{categoria_id}")
async def atualizar_categoria_parcial(categoria_id: int, categoria: CategoriaTransacaoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categoria FROM categoriatransacao WHERE id_categoria = %s", (categoria_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Categoria não encontrada")
    
    fields = []
    values = []
    for campo, valor in categoria.dict(exclude_unset=True).items():
        if campo == "tipo_categoria" and valor not in ['Entrada', 'Saida']:
            cur.close()
            conn.close()
            raise HTTPException(400, "Tipo de categoria deve ser 'Entrada' ou 'Saida'")
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(categoria_id)
    try:
        cur.execute(f"UPDATE categoriatransacao SET {', '.join(fields)} WHERE id_categoria=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Categoria atualizada"}

@router.delete("/{categoria_id}")
async def deletar_categoria(categoria_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categoriatransacao WHERE id_categoria=%s", (categoria_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Categoria removida"}
