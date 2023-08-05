import os
import asyncio
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/')
def welcome():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/messages/")
def add_messages(messages):
    try:
        response_messages = []
        for message in messages:
            response_messages.append({"message": message})
        return response_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))
