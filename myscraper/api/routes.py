import os
import asyncio
from fastapi import FastAPI, HTTPException
from ..database.database import Database

app = FastAPI()
db = Database()
db.create_message_table()

@app.get('/')
def welcome():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/messages/")
def add_messages(messages: list):
    try:
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))
