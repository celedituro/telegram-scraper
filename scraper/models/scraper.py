import json
from loguru import logger

from telethon import TelegramClient, sync
from telethon.tl.types import InputMessagesFilterEmpty

class Scraper:
    """
    A class for scraping Telegram group messages using the Telethon library.

    Args:
        api_id (str): The API ID for the Telethon client.
        api_hash (str): The API hash for the Telethon client.

    Attributes:
        client: The Telethon client used for interacting with Telegram.

    Methods:
        get_client(api_id: str, api_hash: str): Creates and returns a Telethon client.
        get_group_entity(group_username: str): Retrieves the entity of a Telegram group.
        get_group_messages(entity): Retrieves messages from a Telegram group.
        authorize_user(phone_number: str): Authorizes the user using a phone number.
        get_messages_from_group(phone_number: str, group_username: str): Retrieves messages from a group.

    Notes:
        This class uses the Telethon library to interact with Telegram and retrieve group messages.
        It handles user authorization and message retrieval from the specified group.
    """
    
    def __init__(self, api_id: str, api_hash: str):
        """
        Initializes the Telethon client.

        Args:
            api_id (str): The API ID for the Telethon client.
            api_hash (str): The API hash for the Telethon client.
        """
        self.client = self.get_client(api_id, api_hash)

    def get_client(self, api_id: str, api_hash: str):
        """
        Creates and returns a Telethon client.

        Args:
            api_id (str): The API ID for the Telethon client.
            api_hash (str): The API hash for the Telethon client.

        Returns:
            TelegramClient: An instance of the Telethon client.
        """
        try:
            logger.info('[SCRAPER]: getting telegram client')
            return TelegramClient('my_telegram_session', api_id, api_hash)
        except Exception as e:
            raise Exception(e)
            return None

    async def get_group_entity(self, group_username: str):
        """
        Retrieves the entity of a Telegram group.

        Args:
            group_username (str): The username of the group.

        Returns:
            Entity: The entity representing the Telegram group.
        """
        try:
            logger.info('[SCRAPER]: getting group entity')
            return await self.client.get_entity(group_username)    
        except Exception as e:
            raise Exception(e)
            return None
        
    async def get_group_messages(self, entity):
        """
        Retrieves messages from a Telegram group.

        Args:
            entity: The entity representing the Telegram group.

        Returns:
            list: List of messages retrieved from the group.
        """
        try:
            logger.info('[SCRAPER]: getting group messages')
            return await self.client.get_messages(entity, limit=100, filter=InputMessagesFilterEmpty())
        except Exception as e:
            raise Exception(e)
            return None
    
    async def authorize_user(self, phone_number: str):
        """
        Authorizes the user using a phone number.

        Args:
            phone_number (str): The user's phone number.
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
            raise Exception(e)

    async def get_messages_from_group(self, phone_number: str, group_username: str):
        """
        Retrieves messages from a Telegram group.

        Args:
            phone_number (str): The user's phone number for authorization.
            group_username (str): The username of the group.

        Returns:
            list: List of messages retrieved from the group.

        Notes:
            This method coordinates the process of authorizing the user, getting the group entity,
            retrieving messages from the group, and disconnecting the client.
        """
        try:
            await self.authorize_user(phone_number)
            entity = await self.get_group_entity(group_username)
            if entity:
                messages = await self.get_group_messages(entity)
                if messages:
                    self.client.disconnect()
                    return messages
        except Exception as e:
            logger.error(f"[SCRAPER]: {e}")
            raise Exception(e)    
            return None
