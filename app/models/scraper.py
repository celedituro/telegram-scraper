import json
from loguru import logger

from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty

class Scraper:
    def __init__(self, api_id: str, api_hash: str):
        self.client = self.get_client(api_id, api_hash)

    def get_client(self, api_id: str, api_hash: str):
        """
        Get a telegram client to get messages from a group.
        
        Args:
            api_id: credential of a project in telegram.
            api_hash: credential of a project in telegram.
            
        Returns:
            Telegram client.
        """
        try:
            logger.info('[SCRAPER]: getting telegram client')
            return TelegramClient('my_telegram_session', api_id, api_hash)
        except Exception as e:
            logger.error(f"[SCRAPER]:  Error in getting client {e}")

    async def get_group_entity(self, group_username: str):
        """
        Get a telegram entity using its username.
        
        Args:
            group_username: username from a telegram group.
            
        Returns:
            Telegram entity.
        """
        try:
            logger.info('[SCRAPER]: getting group entity')
            return await self.client.get_entity(group_username)    
        except Exception as e:
            logger.error(f"[SCRAPER]: Error in getting group entity {e}")

    async def get_group_messages(self, entity):
        """
        Get all the messages from a telegram entity.
        
        Args:
            entity: telegram entity.
            
        Returns:
            List of telegram messages from the entity.
        """
        try:
            logger.info('[SCRAPER]: getting group messages')
            return await self.client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
        except Exception as e:
            logger.error(f"[SCRAPER]: Error in getting group messages {e}")
    
    async def authorize_user(self, phone_number: str):
        """
        Authenticate a user to create a telegram session.
        
        Args:
            phone_number: phone_number of the user to authenticate from telegram.
            
        Returns:
            List of telegram messages from the entity.
        """
        try:
            await self.client.start()
            if await self.client.is_user_authorized():
                logger.info("[SCRAPER]: user auth already exist")
            else:
                logger.info("[SCRAPER]: start session with phone number")
                await self.client.send_code_request(phone_number)
                code = input("Verification code: ")
                await self.client.sign_in(phone_number, code)
        except Exception as e:
            logger.error(f"[SCRAPER]: Error when auth user {e}")
                        
    async def get_messages_from_group(self, phone_number: str, group_username: str):
        """
        Get all the messages from a given telegram group.
        
        Args:
            phone_number: number of the telegram account associated.
            group_username: username of the group.
            
        Returns:
            List of messages from the telegram group.
        """
        try:
            await self.authorize_user(phone_number)
            entity = await self.get_group_entity(group_username)
            messages = await self.get_group_messages(entity)
            self.client.disconnect()
            return messages
        except Exception as e:
            logger.error(f"[SCRAPER]: Error in getting messages {e}")
    
