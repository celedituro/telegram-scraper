# Telegram Scraper

## Tecnologías

- Python
- PostgreSql
- Docker

## Telegram Bot

Para extraer los mensajes del canal de telegram, se utiliza un bot de telegram.

## Ejecución del programa

**Paso 1)** Clonar el repositorio.

**Paso 2)** Ubicarse en la dirección raíz del proyecto y ejecutar el programa mediante el siguiente comando:

``
docker-compose up
``

**Paso 3)** Abrir telegram, iniciar una conversación con el bot con nombre "scraper_cd_bot" enviadole el comando ``/start`` y, luego, enviarle el comando ``/get_messages`` para obtener el registro de los mensajes del canal.
