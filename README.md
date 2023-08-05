# Telegram Scraper

## Tecnologías

- Python
- PostgreSql
- Docker

## Ejecución del programa

**Paso 1)** Clonar el repositorio.

**Paso 2)** Ubicarse en la dirección raíz del proyecto y ejecutar el programa mediante el siguiente comando:

``
docker-compose up --build
``

## Extracción de mensajes del grupo de Telegram

Para extraer los mensajes del grupo de telegram, se utiliza el script ``client.py``. Al ejecutar este script, se va a crear una sesión de telegram. Para esto es necesario proveer: ``api_id``, ``api_hash`` del proyecto y el ``phone_number`` de la cuenta asociada a telegram. La primera vez que se ejecuta el script, se le va a solicitar al usuario el código de sesión que le llega a su cuenta de telegram. Una vez ingresado el código de sesión, se extraen los mensajes del grupo.

Podes obtener el ``api_id`` y ``api_hash`` del proyecto ingresando a la siguiente página: <https://my.telegram.org/auth>.
  
## Documentación

- <https://docs.telethon.dev/en/stable/index.html>
