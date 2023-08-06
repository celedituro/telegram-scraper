import os
import asyncio
from fastapi import FastAPI, HTTPException
from ..database.database import Database
from ..service.message_service import MessageService

app = FastAPI()
db = Database()
db.create_message_table()
service = MessageService(db)

@app.get('/', status_code=200)
def welcome():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/messages/", status_code=201)
def add_messages(messages: list):
    try:
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))

@app.get("/messages", status_code=200)
def get_all_messages():
    try:
        return service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))
