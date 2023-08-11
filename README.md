# Telegram Channels Scraper

## Tecnologías

- Python
- PostgreSql
- Docker

## Extracción de mensajes del grupo de Telegram

Para extraer los mensajes del grupo de telegram, se utiliza la librería telethon de python. La extracción se implementa por medio del script ``client.py`` ubicado en el directorio ``/app``. Al ejecutar este script, se crea una sesión de telegram de la cuenta asociada a la variable ```PHONE_NUMBER```. Para esto es necesario proveer datos del proyecto como: ``API_ID``, ``API_HASH`` en el archivo ``.env`` (el archivo ``.env.example`` tiene una lista de las variables necesarias para poder ejecutar la aplicación correctamente).

La primera vez que se ejecuta el script ``client.py``, se le solicita al usuario ingresar el código de sesión que le llega a su cuenta de telegram. Una vez ingresado el código de sesión, se extraen los mensajes del grupo definido en la variable ``GROUP_USERNAME`` en el archivo ``.env``.

Los valores ``API_ID`` y ``API_HASH`` de un nuevo proyecto se pueden obtener ingresando a la siguiente página: <https://my.telegram.org/auth>.

## Autenticación de la API

Para poder realizar consultas a la API es necesario registrar y loggear un usuario con ``username`` y ``password`` en la aplicación. De esta manera sólo los usuarios autorizados van a poder realizar consultas a la API.

## Ejecución del Scraper

**Paso 1)** Clonar el repositorio y ubicarse en la dirección raíz del proyecto.

**Paso 2)** Abrir una terminal y ejecutar ``docker-compose up --build`` para poner en ejecución al servidor.

**Paso 3)** Abrir otra terminal, ubicarse en ``/app`` y ejecutar ``poetry run python client.py`` para realizar la extracción de los mensajes del grupo de telegram.
  
Ingresar a ``http://localhost:8000/docs`` para acceder a la documentación de la API. Se puede realizar consultas acerca del historial de mensajes del grupo así como de los links compartidos en el mismo por medio de la misma.

## Ejecución de la regla YARA

**Paso 1)** Ubicarse en el directorio ``/yara``.

**Paso 2)** Ejecutar el script para detectar si se cumple la regla definida en ``mercadolibre.yara``: ``poetry run python detect_rule.py``.

## Documentación

- <https://docs.telethon.dev/en/stable/index.html>
- <https://yara.readthedocs.io/en/stable/>
