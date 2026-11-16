from fastapi import FastAPI

from .database import criar_tabelas
from .routes.registros import router as registros_router

app = FastAPI(
    title="API de Gerenciamento",
    description="API REST organizada em pacotes e protegida por Nginx.",
    version="3.0.0"
)


@app.on_event("startup")
def startup_event():
    criar_tabelas()


app.include_router(registros_router)
