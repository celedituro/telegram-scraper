# Usa la imagen oficial de Python como punto de partida
FROM python:3.9

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos y bloquea la versión de las dependencias de tu proyecto
COPY pyproject.toml poetry.lock ./

# Instala Poetry dentro del contenedor
RUN pip install poetry

# Instala las dependencias del proyecto
RUN poetry install --no-root --no-interaction

# Copia las fuentes de tu aplicación al contenedor
COPY myscraper/main.py .

# Expone el puerto en el que se ejecuta tu aplicación FastAPI (asegúrate de que coincida con el puerto que estás utilizando en tu código)
EXPOSE 8000

# Comando para ejecutar tu aplicación cuando se inicie el contenedor
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]