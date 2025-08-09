from fastapi import FastAPI
import uvicorn

# Importar todos os roteadores dos CRUDs
from Crud_Usuario import router as usuarios_router
from Crud_DetalhesUsuario import router as detalhes_router
from Crud_CategoriaTransacao import router as categorias_router
from Crud_Transacao import router as transacoes_router
from Crud_Produto import router as produtos_router
from Crud_Venda import router as vendas_router
from Crud_Relatorio import router as relatorios_router

# Inicializar FastAPI
app = FastAPI(
    title="FinanCerto API", 
    description="API para sistema de gestão financeira", 
    version="3.0.0"
)

# Registrar todos os roteadores
app.include_router(usuarios_router)
app.include_router(detalhes_router)
app.include_router(categorias_router)
app.include_router(transacoes_router)
app.include_router(produtos_router)
app.include_router(vendas_router)
app.include_router(relatorios_router)

# Endpoint raiz
@app.get("/")
async def root():
    return {
        "message": "FinanCerto API v3.0", 
        "docs": "/docs",
        "description": "API modularizada com CRUDs separados"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
