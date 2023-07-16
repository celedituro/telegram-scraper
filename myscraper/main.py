"""
Mi API con FastAPI

Este módulo contiene la configuración y definición de rutas
para una API sencilla utilizando FastAPI.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    Ruta raíz de la API.

    Esta función maneja las solicitudes HTTP GET en la ruta raíz ("/")
    de la API y devuelve un mensaje de bienvenida.
    """
    return {"Hello": "World"}
