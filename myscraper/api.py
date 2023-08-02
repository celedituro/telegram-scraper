from fastapi import FastAPI, HTTPException
from telethon import TelegramClient, events, utils
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
chat_id = os.environ.get('CHAT_ID')

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome to the telegram channels scraper"}

client = TelegramClient('mysession', api_id, api_hash)

async def get_all_group_messages(client, group_entity, limit=100):
    print('Get all group messages')
    all_messages = []
    last_date = None
    total_messages = 0
    while True:
        messages = await client.get_messages(group_entity, limit=limit, reverse=True, min_date=last_date)
        if not messages:
            break
        all_messages.extend(messages)
        total_messages += len(messages)
        last_date = messages[-1].date
        print("Get {total_messages} messages upto {last_date}")
    return all_messages

@app.get("/telegram/messages")
async def get_telegram_messages():
    try:
        print('Init client')
        client = TelegramClient(None, api_id, api_hash)
        await client.start(phone_number)
        code = input()
        
        print('Get group entity')
        group_entity = await client.get_entity('1737437378')
        print(group_entity)
        
        print('Get all messages')
        messages = await get_all_group_messages(client, group_entity)
        print(messages)

        print('Disconnecting client')
        await client.disconnect()
        print('Client disconnected')

        return messages

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))