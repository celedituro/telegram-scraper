import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..database.database import Database
from ..service.message_service import MessageService
from ..models.message import Message

app = FastAPI()

# Add the middleware of CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = Database()
db.create_message_table()
service = MessageService(db)

@app.get('/', status_code=200)
def welcome():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/message/", status_code=201)
def add_messages(message: Message):
    try:
        service.add_message(message.id, message.content)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200)
def get_all_messages():
    try:
        return service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))
