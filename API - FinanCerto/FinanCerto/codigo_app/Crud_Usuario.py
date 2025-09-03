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
class UsuarioBase(BaseModel):
    nome_usuario: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome_usuario: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int

# Router
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# CRUD para Usuários
@router.post("/", response_model=UsuarioResponse)
async def criar_usuario(usuario: UsuarioCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    # Verificar se email já existe
    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (usuario.email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(400, "Email já cadastrado")
    
    try:
        cur.execute("INSERT INTO usuario (nome_usuario, email, senha) VALUES (%s, %s, %s) RETURNING id_usuario",
                   (usuario.nome_usuario, usuario.email, usuario.senha))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return UsuarioResponse(id_usuario=result[0], nome_usuario=usuario.nome_usuario, email=usuario.email)
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar usuário: {e}")

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(skip: int = 0, limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome_usuario, email FROM usuario ORDER BY id_usuario OFFSET %s LIMIT %s", (skip, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [UsuarioResponse(id_usuario=u[0], nome_usuario=u[1], email=u[2]) for u in rows]

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obter_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nome_usuario, email FROM usuario WHERE id_usuario = %s", (usuario_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return UsuarioResponse(id_usuario=row[0], nome_usuario=row[1], email=row[2])
    raise HTTPException(404, "Usuário não encontrado")

@router.patch("/{usuario_id}")
async def atualizar_usuario_parcial(usuario_id: int, usuario: UsuarioUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s", (usuario_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Usuário não encontrado")
    
    fields = []
    values = []
    for campo, valor in usuario.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(usuario_id)
    try:
        cur.execute(f"UPDATE usuario SET {', '.join(fields)} WHERE id_usuario=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Usuário atualizado"}

@router.delete("/{usuario_id}")
async def deletar_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE id_usuario=%s", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Usuário removido"}
