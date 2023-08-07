import httpx
import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty
import json
import warnings
from models.parser import MessageParser

load_dotenv()
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
group_username = os.environ.get('GROUP_USERNAME')
api_url = os.environ.get('API_URL')

def get_client(api_id, api_hash):
    try:
        print('[CLIENT]: getting telegram client')
        return TelegramClient('my_telegram_session', api_id, api_hash)
    except Exception as e:
        print("[CLIENT]:  Error in getting client: ", str(e))

async def get_group_entity(client, group_username):
    try:
        print('[CLIENT]: getting group entity')
        return await client.get_entity(group_username)    
    except Exception as e:
        print("[CLIENT]: Error in getting group entity: ", str(e))

async def get_group_messages(client, entity):
    try:
        print('[CLIENT]: getting group messages')
        return await client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
    except Exception as e:
       print("[CLIENT]: Error in getting group messages: ", str(e))
    
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
        print("[CLIENT]: Error in getting messages: ", str(e))

def get_parsed_messages(parser, messages):
    data = []
    for message in messages:
        parsed_message = parser.parse_message(message)
        if parsed_message:
            data.append(parsed_message)
    
    return data

async def run_client(parser: MessageParser):
    async with httpx.AsyncClient() as client:
        messages = await get_messages(api_id, api_hash, phone_number, group_username)
        data = get_parsed_messages(parser, messages)  
        for d in data:
            print(f'[CLIENT]: send {d} to server')
            response = await client.post(f'{api_url}/message/', json=d)
            if response.status_code == 201:
                print("[CLIENT]: receive from server:", response.status_code)
            else:
                if response.status_code == 307:
                    new_location = response.headers.get('Location')
                    print(f'[CLIENT]: redirecting request to: {new_location}')
                    response = await client.post(new_location, json=data)
                else:
                    print("[CLIENT]: receive from server:", response.status_code)

if __name__ == '__main__':
    parser = MessageParser()
    asyncio.run(run_client(parser))
