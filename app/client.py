import asyncio
import os
import httpx
import time
from loguru import logger

from dotenv import load_dotenv

from models.parser import MessageParser
from models.scraper import Scraper
from models.user import User

load_dotenv()

API_URL = os.environ.get('API_URL')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME')

REDIRECTION_STATUS_CODE = 307

def get_user_credentials():
    """
    Get username and password from user.
    """
    username = input('Username: ')
    password = input('Password: ')
    user = {
        "username": username,
        "password": password
    }
    return user 

async def handle_response(client, response):
    """
    Handles response from API server.
    
    Args:
        client: async client that make requests.
        response: response from API server when post a message.
    """
    if response.status_code == REDIRECTION_STATUS_CODE:
        new_location = response.headers.get('Location')
        logger.info(f'[CLIENT]: redirecting request to: {new_location}')
        response = await client.post(new_location, json=data)
    logger.info(f"[CLIENT]: receive {response.status_code}")

def parse_messages(messages, parser: MessageParser):
    """
    Parse telegram messages.
    
    Args:
        messages: messages of a group received from telegram.
        parser: parser of telegram messages.
        
    Returns:
        Telegram messages parsed.
    """
    parsed_messages = []
    for message in messages:
        parsed_message = parser.parse_message(message)
        if parsed_message is not None:
            parsed_messages.append(parsed_message)
    return parsed_messages

def save_messages(messages):
    """
    Write messages in a txt file.
    
    Args:
        messages: messages parsed.
        
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
    Post parsed messages to API server.
    
    Args:
        client: async client that makes request.
        messages: parsed messages from the telegram group.
        token: access token of user from API.
    """
    try:
        for parsed_message in parsed_messages:
            if parsed_message:
                id = parsed_message["id"]
                logger.info(f'[CLIENT]: send message {id} to server')
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.post(f'{API_URL}/messages', json=parsed_message, headers=headers)
                await handle_response(client, response)
    except Exception as e:
        logger.error(f"[CLIENT]: Error when posting messages {e}")
        
async def authenticate_user(user, client):
    """
    Authenticate user in API server.
    
    Args:
        user: user to authenticate.
        client: async client that make requests.
        
        
    Returns:
        token: access token of user from API.
    """
    try:
        username = user["username"]
        resp = await client.post(f'{API_URL}/users', json=user)
        if resp.status_code == 201:
            logger.info(f"[CLIENT]: {username} has signup")
        resp = await client.post(f'{API_URL}/users/login', json=user)
        if resp.status_code == 201:
            logger.info(f"[CLIENT]: {username} has logged in")    
        token = resp.json()["token"]
        return token
    except Exception as e:
        logger.error(f"[CLIENT]: Error when auth user in API {e}")      
          
async def run(scraper: Scraper, parser: MessageParser, user: User):
    """
    Post all the messages from a telegram group to the API server.
    
    Args:
        scraper: entity that gets the messages from the telegram group.
        parser: entity that parses telegram messages.
        user: user to be authenticate in the API.
    """
    async with httpx.AsyncClient() as client:
        try:
            token = await authenticate_user(user, client)
            messages = await scraper.get_messages_from_group(PHONE_NUMBER, GROUP_USERNAME)
            parsed_messages = parse_messages(messages, parser)
            save_messages(parsed_messages)
            await post_messages(client, parsed_messages, token)
        except Exception as e:
            logger.error(f"[CLIENT]: Error when running client {e}")      
         
if __name__ == '__main__':
    user = get_user_credentials()
    scraper = Scraper(API_ID, API_HASH)
    parser = MessageParser()
    asyncio.run(run(scraper, parser, user))
