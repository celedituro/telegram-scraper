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
from utils.constants import API_URL

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME')

REDIRECTION_STATUS_CODE = 307

async def handle_response(client, response):
    """
    Handles the response from an API server after posting a message.
    
    Args:
        client: An asynchronous client used to make requests.
        response: The response received from the API server.
        
    Notes:
        If the response status code indicates redirection, the function will follow
        the redirection by sending a POST request to the new location.
    """
    while response.status_code == REDIRECTION_STATUS_CODE:
        new_location = response.headers.get('Location')
        logger.info(f'[CLIENT]: redirecting request to: {new_location}')
        response = await client.post(new_location, json=data)
    logger.info(f"[CLIENT]: receive {response.status_code}")
                 
async def post_messages(client, parsed_messages, token: str):
    """
    Posts parsed messages to a server.
    
    Args:
        client: An asynchronous client for making requests.
        parsed_messages (list): List of parsed messages to be posted.
        token (str): Authentication token for the server.
    
    Notes:
        This function iterates through the parsed messages, sends each message to the server with the
        authentication token, and handles the server's response using the handle_response function.
    """
    try:
        for parsed_message in parsed_messages:
            if parsed_message:
                id = parsed_message["id"]
                headers = {"Authorization": f"Bearer {token}"}
                logger.info(f'[CLIENT]: post message {id}')
                response = await client.post(f'{API_URL}/messages', json=parsed_message, headers=headers)
                await handle_response(client, response)
    except httpx.RequestError as request_error:
        logger.error(f"[CLIENT]: {request_error}")
    except Exception as e:
        logger.error(f"[CLIENT]: Error when posting messages {e}")     
          
async def run(scraper: Scraper, parser: MessageParser, user_auth: UserAuth, file_saver: FileSaver, user: User):
    """
    Runs the client process.
    
    Args:
        scraper: A scraper for obtaining messages.
        parser: A parser for processing messages.
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
                parsed_messages = parser.parse_messages(messages)
                file_saver.save_messages(parsed_messages)
                await post_messages(client, parsed_messages, token)
        except httpx.RequestError as request_error:
            logger.error(f"[CLIENT]: {request_error}")
        except Exception as e:
            logger.error(f"[CLIENT]: {e}")      
         
if __name__ == '__main__':
    try:
        controller = InputController()
        user = controller.get_user_credentials()
        if user:
            scraper = Scraper(API_ID, API_HASH)
            parser = MessageParser()
            user_auth = UserAuth()
            file_saver = FileSaver()
            asyncio.run(run(scraper, parser, user_auth, file_saver, user))
    except Exception as e:
        logger.error(f"[CLIENT]: {e}")      
