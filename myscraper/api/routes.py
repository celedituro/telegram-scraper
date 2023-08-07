import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..database.database import Database
from ..service.service import MessageService
from ..models.message import Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')

app = FastAPI()

# Add the middleware of CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = Database(db_name, db_user, db_password, db_host, db_port)
db.create_message_table()
service = MessageService(db)

@app.get('/', status_code=200)
def welcome():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/message/", status_code=201)
def add_messages(message: Message):
    try:
        service.add_message(message.id, message.channel_id, message.content, message.date)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200)
def get_all_messages():
    try:
        return service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))
