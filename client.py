import httpx
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty
import json

load_dotenv()
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
group_username = os.environ.get('GROUP_USERNAME')

def get_client(api_id, api_hash):
    try:
        return TelegramClient('my_telegram_session', api_id, api_hash)
    except Exception as e:
        print("Error in getting client: ", str(e))
        raise HTTPException(status_code=500, detail=' ' + str(e))

async def get_group_entity(client, group_username):
    try:
        return await client.get_entity(group_username)    
    except Exception as e:
        print("Error in getting group entity: ", str(e))

async def get_group_messages(client, entity):
    try:
        return await client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
    except Exception as e:
       print("Error in getting group messages: ", str(e))
    
async def get_messages(api_id, api_hash, phone_number, group_username):
    try:
        client = get_client(api_id, api_hash)
        print('client:', client)
        await client.start(phone_number)
        entity = await get_group_entity(client, group_username)
        print('entity:', entity)
        messages = await get_group_messages(client, entity)
        print('messages: ', messages)
        return messages
    except Exception as e:
        print("Error in getting messages: ", str(e))

async def run_client():
    async with httpx.AsyncClient() as client:
        data = await get_messages(api_id, api_hash, phone_number, group_username)
        #response = await client.post('http://localhost:8000/messages', json=data)
        #if response.status_code == 200:
        #    data = response.json()
        #    print("Response from server:", data)
        #else:
        #    print("Error: ", response.status_code)

if __name__ == '__main__':
    asyncio.run(run_client())
