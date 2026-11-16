
import sqlite3
from fastapi import FastAPI, HTTPException

from database import get_db_connection, criar_tabelas
from models import RegistroBase, RegistroResponse


app = FastAPI(
    title="API de Gerenciamento - Projeto A4",
    description="API REST organizada em múltiplas camadas.",
    version="2.0.0"
)


@app.on_event("startup")
def startup_event():
    criar_tabelas()


# POST - Cadastrar registro
@app.post("/registros", response_model=RegistroResponse, status_code=201)
def criar_registro(registro: RegistroBase):

    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="Título não pode estar vazio.")

    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registros (titulo, descricao, ativo) VALUES (?, ?, ?)",
            (registro.titulo, registro.descricao, registro.ativo)
        )
        conn.commit()
        novo_id = cursor.lastrowid

        return {**registro.model_dump(), "id": novo_id}

    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Erro no banco de dados.")

    finally:
        conn.close()


# GET - Listar registros
@app.get("/registros", response_model=list[RegistroResponse])
def listar_registros():

    conn = get_db_connection()

    try:
        registros = conn.execute("SELECT * FROM registros").fetchall()
        return [dict(reg) for reg in registros]

    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Erro ao listar registros.")

    finally:
        conn.close()


# GET - Buscar registro por ID
@app.get("/registros/{registro_id}", response_model=RegistroResponse)
def buscar_registro(registro_id: int):

    conn = get_db_connection()

    try:
        registro = conn.execute(
            "SELECT * FROM registros WHERE id = ?",
            (registro_id,)
        ).fetchone()

        if registro is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado.")

        return dict(registro)

    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Erro ao buscar registro.")

    finally:
        conn.close()


# PUT - Atualizar registro
@app.put("/registros/{registro_id}", response_model=RegistroResponse)
def atualizar_registro(registro_id: int, registro: RegistroBase):

    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="Título não pode estar vazio.")

    conn = get_db_connection()

    try:
        existente = conn.execute(
            "SELECT * FROM registros WHERE id = ?",
            (registro_id,)
        ).fetchone()

        if existente is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado.")

        conn.execute(
            "UPDATE registros SET titulo = ?, descricao = ?, ativo = ? WHERE id = ?",
            (registro.titulo, registro.descricao, registro.ativo, registro_id)
        )
        conn.commit()

        return {**registro.model_dump(), "id": registro_id}

    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Erro ao atualizar registro.")

    finally:
        conn.close()


# DELETE - Excluir registro
@app.delete("/registros/{registro_id}")
def deletar_registro(registro_id: int):

    conn = get_db_connection()

    try:
        existente = conn.execute(
            "SELECT * FROM registros WHERE id = ?",
            (registro_id,)
        ).fetchone()

        if existente is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado.")

        conn.execute(
            "DELETE FROM registros WHERE id = ?",
            (registro_id,)
        )
        conn.commit()

        return {"mensagem": "Registro removido com sucesso."}

    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Erro ao excluir registro.")

    finally:
        conn.close()
