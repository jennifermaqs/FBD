from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import date
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
class DetalhesUsuarioBase(BaseModel):
    data_nascimento: Optional[date] = None
    telefone_contato: Optional[str] = None
    cpf: Optional[str] = None
    nome_negocio: Optional[str] = None

class DetalhesUsuarioCreate(DetalhesUsuarioBase):
    id_usuario: int

class DetalhesUsuarioUpdate(BaseModel):
    data_nascimento: Optional[date] = None
    telefone_contato: Optional[str] = None
    cpf: Optional[str] = None
    nome_negocio: Optional[str] = None

class DetalhesUsuarioResponse(DetalhesUsuarioBase):
    id_usuario: int

# Router
router = APIRouter(prefix="/detalhes-usuario", tags=["Detalhes do Usuário"])

# CRUD para Detalhes do Usuário
@router.post("/", response_model=DetalhesUsuarioResponse)
async def criar_detalhes_usuario(detalhes: DetalhesUsuarioCreate):
    conn = get_connection()
    cur = conn.cursor()
    
    # Verificar se usuário existe
    cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s", (detalhes.id_usuario,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Usuário não encontrado")
    
    try:
        cur.execute(
            """INSERT INTO detalhesusuario (id_usuario, data_nascimento, telefone_contato, cpf, nome_negocio) 
               VALUES (%s, %s, %s, %s, %s)""",
            (detalhes.id_usuario, detalhes.data_nascimento, detalhes.telefone_contato, 
             detalhes.cpf, detalhes.nome_negocio)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return DetalhesUsuarioResponse(
            id_usuario=detalhes.id_usuario,
            data_nascimento=detalhes.data_nascimento,
            telefone_contato=detalhes.telefone_contato,
            cpf=detalhes.cpf,
            nome_negocio=detalhes.nome_negocio
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(400, f"Erro ao criar detalhes: {e}")

@router.get("/{usuario_id}", response_model=DetalhesUsuarioResponse)
async def obter_detalhes_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, data_nascimento, telefone_contato, cpf, nome_negocio FROM detalhesusuario WHERE id_usuario = %s", (usuario_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if row:
        return DetalhesUsuarioResponse(
            id_usuario=row[0],
            data_nascimento=row[1],
            telefone_contato=row[2],
            cpf=row[3],
            nome_negocio=row[4]
        )
    raise HTTPException(404, "Detalhes do usuário não encontrados")

@router.patch("/{usuario_id}")
async def atualizar_detalhes_parcial(usuario_id: int, detalhes: DetalhesUsuarioUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario FROM detalhesusuario WHERE id_usuario = %s", (usuario_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Detalhes do usuário não encontrados")
    
    fields = []
    values = []
    for campo, valor in detalhes.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    
    values.append(usuario_id)
    try:
        cur.execute(f"UPDATE detalhesusuario SET {', '.join(fields)} WHERE id_usuario=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    
    return {"msg": "Detalhes do usuário atualizados"}

@router.delete("/{usuario_id}")
async def deletar_detalhes_usuario(usuario_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM detalhesusuario WHERE id_usuario=%s", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Detalhes do usuário removidos"}
