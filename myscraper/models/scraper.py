import json
import warnings

from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty

from models.parser import MessageParser

class Scraper:
    def __init__(self, api_id, api_hash):
        self.client = self.get_client(api_id, api_hash)

    def get_client(self, api_id, api_hash):
        try:
            print('[SCRAPER]: getting telegram client')
            return TelegramClient('my_telegram_session', api_id, api_hash)
        except Exception as e:
            print("[SCRAPER]:  Error in getting client: ", str(e))

    async def get_group_entity(self, group_username):
        try:
            print('[SCRAPER]: getting group entity')
            return await self.client.get_entity(group_username)    
        except Exception as e:
            print("[SCRAPER]: Error in getting group entity: ", str(e))

    async def get_group_messages(self, entity):
        try:
            print('[SCRAPER]: getting group messages')
            return await self.client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
        except Exception as e:
            print("[SCRAPER]: Error in getting group messages: ", str(e))
    
    async def get_messages(self, phone_number, group_username):
        try:
            warnings.filterwarnings("ignore", category=UserWarning)
            await self.client.start(phone_number)
            entity = await self.get_group_entity(group_username)
            messages = await self.get_group_messages(entity)
            #client.disconnect()
            return messages
        except Exception as e:
            print("[SCRAPER]: Error in getting messages: ", str(e))
    
