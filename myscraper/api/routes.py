import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import List
from psycopg2 import IntegrityError

from ..database.database import Database
from ..services.message_service import MessageService
from ..models.presenter import Presenter
from ..models.parser import MessageParser
from ..models.message import Message, LinkMessage

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

app = FastAPI()

# Add the middleware of CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
db.create_messages_table()
db.create_users_table()

parser = MessageParser()
presenter = Presenter()
service = MessageService(db, parser, presenter)

post_responses = {
    201: {"description": "Created", "model": Message},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Message already exists"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}

get_responses = {
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
}

@app.get('/', status_code=200)
def read_root():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/message/", status_code=201, response_model=Message, responses=post_responses)
async def add_message(message: Message):
    """
    Create a new message.
    """
    try:
        return await service.add_message(message)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Message already exists", headers={"X-Error": "ItemDuplicate"})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200, response_model=List[Message], responses=get_responses)
def get_all_messages():
    """
    Get a list of messages.
    """
    try:
        return service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))

@app.get("/messages/link", status_code=200, response_model=List[LinkMessage], responses=get_responses)
def get_link_messages():
    """
    Get a list of link messages.
    """
    try:
        return service.get_link_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting link messages: ' + str(e))
