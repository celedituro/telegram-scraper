# Usa la imagen oficial de Python como punto de partida
FROM python:3

# Directorio de trabajo dentro del contenedor
WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

# Copia los archivos de requerimientos y bloquea la versión de las dependencias de tu proyecto
COPY pyproject.toml poetry.lock ./

# Instala Poetry dentro del contenedor
RUN pip install poetry

# Instala las dependencias del proyecto
RUN poetry install --no-root --no-interaction

# Copia todas las fuentes de tu aplicación al contenedor
COPY . /app

# Expone el puerto en el que se ejecuta tu aplicación FastAPI (asegúrate de que coincida con el puerto que estás utilizando en tu código)
EXPOSE 8000

# Ejecuta los comandos al inicializar el contenedor
CMD ["sh", "-c", "poetry run pytest tests && poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000"]
