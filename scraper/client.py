import asyncio
import os
import httpx
from loguru import logger
from dotenv import load_dotenv
import sys
sys.path.append("..")

from models.parser import MessageParser
from models.scraper import Scraper
from api.models.data_models import User
from models.input_controller import InputController
from models.user_auth import UserAuth
from models.file_saver import FileSaver
from models.handler import MessageHandler
from api.exceptions.user_exceptions import IncorrectPassword

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME')

async def run(scraper: Scraper, parser: MessageParser, user_auth: UserAuth, file_saver: FileSaver, handler: MessageHandler, user: User):
    """
    Runs the client process.
    
    Args:
        scraper: A scraper for obtaining messages.
        parser: A parser for processing messages.
        user_auth: A user authenticator for authenticating a user.
        file_saver: A file saver for saving messages to a file.
        user (dict): User information including username and password.
    
    Notes:
        This function orchestrates the entire client process, including user authentication,
        message scraping, parsing, saving, and posting. Logs information about the process.
    """
    async with httpx.AsyncClient() as client:
        try:
            token = await user_auth.auth_user(client, user)
            if token:
                messages = await scraper.get_messages_from_group(PHONE_NUMBER, GROUP_USERNAME)
                if messages:
                    parsed_messages = parser.parse_messages(messages)
                    if parsed_messages:
                        file_saver.save_messages(parsed_messages)
                        await handler.post_messages(client, parsed_messages, token)
            else:
                raise IncorrectPassword("the password is incorrect")
        except httpx.RequestError as request_error:
            logger.error(f"[CLIENT]: {request_error}")
        except Exception as e:
            raise Exception(e)  
         
if __name__ == '__main__':
    try:
        controller = InputController()
        user = controller.get_user_credentials()
        if user:
            scraper = Scraper(API_ID, API_HASH)
            parser = MessageParser()
            user_auth = UserAuth()
            file_saver = FileSaver()
            handler = MessageHandler()
            asyncio.run(run(scraper, parser, user_auth, file_saver, handler, user))
    except Exception as e:
        logger.error(f"[CLIENT]: {e}")      
