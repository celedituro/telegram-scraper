# Telegram Channels Scraper

## Tecnologías

- Python (v3.11.4)
- PostgreSql (v15.2)
- Docker (v23.0.5)

## API

### Ejecución de la API

**Paso 1)** Clonar el repositorio y ubicarse en la dirección raíz del proyecto.

**Paso 2)** Crear un archivo con nombre ``.env`` con todas las variables definidas en el archivo ``.env.example`` y con sus valores correspondientes.

**Paso 3)** Abrir una terminal y ejecutar el comando ``docker-compose up --build`` para levantar el servidor de la API.

## Scraper

### Extracción de mensajes del grupo de Telegram

Para extraer los mensajes del grupo de Telegram, se utiliza la librería `Telethon` de python. La extracción se implementa por medio del archivo `client.py` ubicado en el directorio `/scraper`. Al ejecutar este archivo, se crea una sesión de Telegram de la cuenta asociada a la variable `PHONE_NUMBER`. Para esto es necesario definir datos del proyecto como el `API_ID` y el `API_HASH` en el archivo `.env` (al igual que el `PHONE_NUMBER`).

La primera vez que se ejecuta el archivo `client.py`, se le solicita al usuario ingresar el `código de verificación` que le llega a su cuenta de Telegram así como la `contraseña` de su cuenta de Telegram. Una vez ingresado el código de sesión, se extraen los mensajes del grupo definido en la variable `GROUP_USERNAME` en el archivo `.env`.

Los valores `API_ID` y `API_HASH` de un nuevo proyecto se pueden obtener ingresando a la siguiente página: <https://my.telegram.org/auth>.

### Ejecución del Scraper

Una vez levantado el servidor de la API:

**Paso 1)** Ubicarse en el directorio raíz del repositorio, abrir una nueva terminal, crear un entorno virtual mediante el siguiente comando `python -m venv myenv` y activarlo por medio del comando
`.\myenv\Scripts\Activate`. (Tener en cuenta que estos comandos corresponden a una máquina con sistema operativo Windows).

**Paso 2)** Ejecutar el comando `pip install -r requirements.txt` para instalar las dependencias necesarias para ejecutar el Scraper.

**Paso 3)** Ubicarse en el directorio `/scraper` y ejecutar el comando `python client.py` para extraer los mensajes del grupo de Telegram. Se le va a solicitar al usuario ingresar ``username`` y ``password`` para registrarse en la API y poder crear mensajes.

**Paso 4)** Ejecutar el comando `deactivate` para desactivar el entorno virtual.

### Autenticación de la API

Para poder realizar consultas a la API es necesario registrar y loggear un usuario con ``username`` y ``password`` en la aplicación. De esta manera sólo los usuarios autorizados van a poder realizar consultas a la API.

**Paso 1)** Ingresar a ``http://localhost:8000/docs``.

**Paso 2)** Registrar un usuario con ``username`` y ``password`` con el endpoint ``POST /users`` (o utilizar las credenciales ingresadas al ejecutar el Scraper).

**Paso 3)** Loggear el usuario registrado para obtener el ``token`` de acceso con el endpoint ``POST /users/login``.

**Paso 4)** Copiar el token recibido al loggear el usuario y pegarlo en la sección ``Authorize`` que se encuentra en la parte superior de la documentación de la API.

**Paso 5)** Realizar una consulta: ``GET /messages`` para extraer todos los mensajes del canal de Telegram o ``GET /messages/link`` para extraer todos los links compartidos en el canal de Telegram. Si el token expira, repetir los pasos 2 y 3.

*Notas*:
Los mensajes del grupo se van a extraer una vez que se ejecuta el Scraper.

## YARA

### Ejecución de la regla YARA

Una vez creado y activado el entorno virutal así como extraídos los mensajes del grupo de Telegram:

**Paso 1)** Abrir una nueva terminal (asegurarse de estar dentro del entorno virtual, caso contrario activarlo) y ubicarse en el directorio `/yara`.

**Paso 2)** Ejecutar el comando `python detect_rule.py` para ejecutar la regla.

**Paso 3)** Ejecutar el comando `deactivate` para desactivar el entorno virtual.

*Notas*:
Es importante haber ejecutado el Scraper previamente a ejecutar la regla de YARA ya que durante la ejecución del Scraper se guardan los mensajes extraídos del canal de Telegram en un archivo de texto con nombre `messages.txt` (en el directorio `/scraper`) y el mismo se utiliza para ejecutar la regla. También es importante instalar las dependencias que se encuentran el archivo `requirements.txt` en el entorno virtual para poder ejecutar la regla correctamente.

## Informe

En el siguiente link se encuentra un informe sobre el canal de telegram analizado así como de los mensajes que se extrayeron del mismo:
[Link al informe](https://github.com/celedituro/telegram-scraper/blob/main/Informe.pdf)
