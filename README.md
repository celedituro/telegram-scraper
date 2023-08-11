# Telegram Channels Scraper

## Tecnologías

- Python (v3.11.4)
- PostgreSql (v15.2)
- Docker (v23.0.5)

## Extracción de mensajes del grupo de Telegram

Para extraer los mensajes del grupo de telegram, se utiliza la librería ``Telethon`` de python. La extracción se implementa por medio del archivo ``client.py`` ubicado en el directorio ``/app``. Al ejecutar este archivo, se crea una sesión de telegram de la cuenta asociada a la variable ```PHONE_NUMBER```. Para esto es necesario definir datos del proyecto como el ``API_ID`` y el ``API_HASH`` en el archivo ``.env`` (al igual que el ``PHONE_NUMBER`` así como el resto de las variables definidas en el archivo 
 ``.env.example``).

La primera vez que se ejecuta el archivo ``client.py``, se le solicita al usuario ingresar el código de sesión que le llega a su cuenta de telegram. Una vez ingresado el código de sesión, se extraen los mensajes del grupo definido en la variable ``GROUP_USERNAME`` en el archivo ``.env``.

Los valores ``API_ID`` y ``API_HASH`` de un nuevo proyecto se pueden obtener ingresando a la siguiente página: <https://my.telegram.org/auth>.

## Autenticación de la API

Para poder realizar consultas a la API es necesario registrar y loggear un usuario con ``username`` y ``password`` en la aplicación. De esta manera sólo los usuarios autorizados van a poder realizar consultas a la API.

## Ejecución del Scraper

**Paso 1)** Clonar el repositorio y ubicarse en la dirección raíz del proyecto.

**Paso 2)** Crear un archivo con nombre ``.env`` con todas las variables definidas en el archivo ``.env.example`` y con sus valores correspondientes.

**Paso 3)** Abrir una terminal y ejecutar el comando ``docker-compose up --build`` para levantar el servidor de la API.

**Paso 4)** Abrir otra terminal y ejecutar el comando ``poetry install`` para instalar todas las dependencias del proyecto.

**Paso 5)** En esa nueva terminarl ubicarse en el directorio ``/app`` y ejecutar el comando ``poetry run python client.py`` para estraer los mensajes del grupo de telegram.
  
Ingresar a ``http://localhost:8000/docs`` para acceder a la documentación de la API. Se pueden realizar consultas acerca del historial de mensajes del grupo así como de los links compartidos en el mismo por medio de la misma.

## Ejecución de la regla YARA

**Paso 1)** Abrir una terminal y ejecutar ``poetry install`` para instalar todas las dependencias del proyecto.

**Paso 2)** Ubicarse en el directorio ``/yara`` y ejecutar el comando ``poetry run python detect_rule.py``.

## Informe

[[Link al informe](../../../Downloads/Informe.pdf)](https://github.com/celedituro/telegram-scraper/blob/main/Informe.pdf)

## Documentación

- <https://docs.telethon.dev/en/stable/index.html>
- <https://yara.readthedocs.io/en/stable/>
