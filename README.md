# Telegram Channels Scraper

## Tecnologías

- Python (v3.11.4)
- PostgreSql (v15.2)
- Docker (v23.0.5)

## API

## Ejecución de la API

**Paso 1)** Clonar el repositorio y ubicarse en la dirección raíz del proyecto.

**Paso 2)** Crear un archivo con nombre ``.env`` con todas las variables definidas en el archivo ``.env.example`` y con sus valores correspondientes.

**Paso 3)** Abrir una terminal y ejecutar el comando ``docker-compose up --build`` para levantar el servidor de la API.

### Autenticación de la API

Para poder realizar consultas a la API es necesario registrar y loggear un usuario con ``username`` y ``password`` en la aplicación. De esta manera sólo los usuarios autorizados van a poder realizar consultas a la API.

**Paso 1)** Ingresar a ``http://localhost:8000/docs``.

**Paso 2)** Registrar un usuario con ``username`` y ``password`` con el endpoint ``POST /users``.

**Paso 3)** Loggear el usuario registrado para obtener el ``token`` de acceso con el endpoint ``POST /users/login``.

**Paso 4)** Copiar el token recibido al loggear el usuario y pegarlo en la sección ``Authorize`` que se encuentra en la parte superior de la documentación de la API.

**Paso 5)** Realizar una consulta: ``GET /messages`` para extraer todos los mensajes del canal de Telegram o ``GET /messages/link`` para extraer todos los links compartidos en el canal de Telegram. Si el token expira, repetir los pasos 2 y 3.

## Scraper

### Extracción de mensajes del grupo de Telegram

Para extraer los mensajes del grupo de Telegram, se utiliza la librería ``Telethon`` de python. La extracción se implementa por medio del archivo ``client.py`` ubicado en el directorio ``/scraper``. Al ejecutar este archivo, se crea una sesión de Telegram de la cuenta asociada a la variable ```PHONE_NUMBER```. Para esto es necesario definir datos del proyecto como el ``API_ID`` y el ``API_HASH`` en el archivo ``.env`` (al igual que el ``PHONE_NUMBER`` así como el resto de las variables definidas en el archivo
 ``.env.example``).

La primera vez que se ejecuta el archivo ``client.py``, se le solicita al usuario ingresar el código de sesión que le llega a su cuenta de telegram. Una vez ingresado el código de sesión, se extraen los mensajes del grupo definido en la variable ``GROUP_USERNAME`` en el archivo ``.env``.

Los valores ``API_ID`` y ``API_HASH`` de un nuevo proyecto se pueden obtener ingresando a la siguiente página: <https://my.telegram.org/auth>.

### Ejecución del Scraper

Una vez levantado el servidor de la API:

**Paso 1)** Abrir una nueva terminal, ubicarse en el directorio ``/scraper`` y ejecutar el comando ``pip install -r requirements_scraper.txt`` para instalar las dependencias necesarias para ejecutar el scraper.

**Paso 2)** Ejecutar el comando ``python client.py`` para extraer los mensajes del grupo de Telegram.
  
Ingresar a ``http://localhost:8000/docs`` para acceder a la documentación de la API. Se pueden realizar consultas acerca del historial de mensajes del grupo así como de los links compartidos en el mismo por medio de la misma.

## YARA

### Ejecución de la regla YARA

**Paso 1)** Abrir una nueva terminal, ubicarse en el directorio ``/yara`` y ejecutar ``pip install -r requirements_yara.txt`` para instalar todas las dependencias necesarias para ejecutar la regla.

**Paso 2)** Ejecutar el comando ``python detect_rule.py`` para ejecutar la regla.

## Informe

En el siguiente link se encuentra un informe sobre el canal de telegram analizado así como de los mensajes que se extrayeron del mismo:
[Link al informe](https://github.com/celedituro/telegram-scraper/blob/main/Informe.pdf)

## Documentación

- <https://docs.telethon.dev/en/stable/index.html>
- <https://yara.readthedocs.io/en/stable/>
