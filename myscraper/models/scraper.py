import httpx
import json
import warnings
import os

from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty
from dotenv import load_dotenv

from models.parser import MessageParser

load_dotenv()
API_URL = os.environ.get('API_URL')

class Scraper:
    def __init__(self, api_id, api_hash):
        self.client = self.get_client(api_id, api_hash)

    def get_client(self, api_id, api_hash):
        try:
            print('[TELEGRAM CLIENT]: getting telegram client')
            return TelegramClient('my_telegram_session', api_id, api_hash)
        except Exception as e:
            print("[TELEGRAM CLIENT]:  Error in getting client: ", str(e))

    async def get_group_entity(self, group_username):
        try:
            print('[CLIENT]: getting group entity')
            return await self.client.get_entity(group_username)    
        except Exception as e:
            print("[CLIENT]: Error in getting group entity: ", str(e))

    async def get_group_messages(self, entity):
        try:
            print('[CLIENT]: getting group messages')
            return await self.client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
        except Exception as e:
            print("[CLIENT]: Error in getting group messages: ", str(e))
    
    async def get_messages(self, phone_number, group_username):
        try:
            warnings.filterwarnings("ignore", category=UserWarning)
            await self.client.start(phone_number)
            entity = await self.get_group_entity(group_username)
            messages = await self.get_group_messages(entity)
            #client.disconnect()
            return messages
        except Exception as e:
            print("[CLIENT]: Error in getting messages: ", str(e))

    async def handle_response(self, c, response):
        if response.status_code == 307:
            new_location = response.headers.get('Location')
            print(f'[CLIENT]: redirecting request to: {new_location}')
            response = await c.post(new_location, json=data)
            print("[CLIENT]: receive from server:", response.status_code)
        else:
            print("[CLIENT]: receive from server:", response.status_code)
            
    async def run(self, parser: MessageParser, phone_number, group_username):
        async with httpx.AsyncClient() as c:
            messages = await self.get_messages(phone_number, group_username)
            for message in messages:
                parsed_message = parser.parse_message(message)
                if parsed_message:
                    print(f'[CLIENT]: send {parsed_message} to server')
                    response = await c.post(f'{API_URL}/messages', json=parsed_message)
                    await self.handle_response(c, response)
    
