import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import List

from ..database.database import Database
from ..service.service import MessageService
from ..models.presenter import Presenter
from ..models.parser import MessageParser
from ..models.message import Message, LinkMessage

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
parser = MessageParser()
presenter = Presenter()
service = MessageService(db, parser, presenter)

@app.get('/', status_code=200)
def read_root():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/message/", status_code=201, response_model=Message)
async def add_message(message: Message):
    """
    Create a new message.
    """
    try:
        return await service.add_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200, response_model=List[Message])
def get_all_messages():
    """
    Get a list of messages.
    """
    try:
        return service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))

@app.get("/messages/link", status_code=200, response_model=List[LinkMessage])
def get_link_messages():
    """
    Get a list of link messages.
    """
    try:
        return service.get_link_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting link messages: ' + str(e))
