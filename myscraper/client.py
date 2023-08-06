import httpx
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty
import json
import warnings

load_dotenv()
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
group_username = os.environ.get('GROUP_USERNAME')
api_url = os.environ.get('API_URL')

def get_client(api_id, api_hash):
    try:
        print('Getting telegram client')
        return TelegramClient('my_telegram_session', api_id, api_hash)
    except Exception as e:
        print("Error in getting client: ", str(e))

async def get_group_entity(client, group_username):
    try:
        print('Getting group entity')
        return await client.get_entity(group_username)    
    except Exception as e:
        print("Error in getting group entity: ", str(e))

async def get_group_messages(client, entity):
    try:
        print('Getting group messages')
        return await client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
    except Exception as e:
       print("Error in getting group messages: ", str(e))
    
async def get_messages(api_id, api_hash, phone_number, group_username):
    try:
        warnings.filterwarnings("ignore", category=UserWarning)
        client = get_client(api_id, api_hash)
        await client.start(phone_number)
        entity = await get_group_entity(client, group_username)
        messages = await get_group_messages(client, entity)
        #client.disconnect()
        return messages
    except Exception as e:
        print("Error in getting messages: ", str(e))

def parse_messages(messages):
    data = []
    for message in messages:
        msg = {
            "id": message.id,
            "content": message.message,
        }
        data.append(msg)
    
    return data

async def run_client():
    async with httpx.AsyncClient() as client:
        messages = await get_messages(api_id, api_hash, phone_number, group_username)
        data = parse_messages(messages)
        response = await client.post(f'{api_url}/messages', json=data)
        if response.status_code == 200:
            data = response.json()
            print("Response from server:", data)
        else:
            if response.status_code == 307:
                new_location = response.headers.get('Location')
                print(f'Redirecting to: {new_location}')
                response = await client.post(new_location, json=data)
                print("Response from server:", data)
            else:
                print("Error: ", response.status_code)

if __name__ == '__main__':
    asyncio.run(run_client())
