import asyncio
import os
import httpx
import time
from loguru import logger
from dotenv import load_dotenv
import sys
sys.path.append("..")

from models.parser import MessageParser
from models.scraper import Scraper
from api.models.data_models import User
from models.input_controller import InputController
from models.user_auth import UserAuth

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

def save_messages(messages):
    """
    Saves parsed messages to a file.
    
    Args:
        messages (list): List of messages to be saved.
    
    Notes:
        This function writes the content of each message in the list to a file named 'messages.txt'.
        Each message's content is written on a new line.
    """
    try:
        with open('messages.txt', 'w', encoding='utf-8') as file:
            for message in messages:
                file.write(message["content"] + '\n')
                time.sleep(1)
        logger.info("[CLIENT]: all messages has been wrote in file")
    except Exception as e:
        logger.error(f"[CLIENT]: Error when writing messages in file {e}")
             
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
                response = await client.post('http://localhost:8000/messages', json=parsed_message, headers=headers)
                await handle_response(client, response)
                logger.info(f'[CLIENT]: message {id} posted')
    except Exception as e:
        logger.error(f"[CLIENT]: Error when posting messages {e}")     
          
async def run(scraper: Scraper, parser: MessageParser, user_auth: UserAuth, user: User):
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
                save_messages(parsed_messages)
                await post_messages(client, parsed_messages, token)
        except Exception as e:
            logger.error(f"[CLIENT]: {e}")      
         
if __name__ == '__main__':
    controller = InputController()
    user = controller.get_user_credentials()
    if user:
        scraper = Scraper(API_ID, API_HASH)
        parser = MessageParser()
        user_auth = UserAuth()
        asyncio.run(run(scraper, parser, user_auth, user))
