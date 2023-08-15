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

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME')

REDIRECTION_STATUS_CODE = 307

def get_user_credentials():
    """
    This function prompts the user for a username and password,
    and returns a dictionary containing these values.

    Returns:
    dict: A dictionary with the user credentials in the following format:
        {
            "username": <username>,
            "password": <password>
        }
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
    Handles the response from an API server after posting a message.
    
    Args:
        client: An asynchronous client used to make requests.
        response: The response received from the API server.
        
    Notes:
        If the response status code indicates redirection, the function will follow
        the redirection by sending a POST request to the new location.
    """
    if response.status_code == REDIRECTION_STATUS_CODE:
        new_location = response.headers.get('Location')
        logger.info(f'[CLIENT]: redirecting request to: {new_location}')
        response = await client.post(new_location, json=data)
    logger.info(f"[CLIENT]: receive {response.status_code}")

def parse_messages(messages, parser: MessageParser):
    """
    Parses Telegram messages using a specified parser.
    
    Args:
        messages (list): List of messages from a Telegram group.
        parser (MessageParser): An instance of the message parser for Telegram messages.
        
    Returns:
        list: Parsed Telegram messages.
        
    Notes:
        This function iterates through the provided list of messages and uses the provided
        parser to parse each message. If a parsed message is obtained from the parser,
        it is added to the list of parsed messages.
    """
    parsed_messages = []
    for message in messages:
        parsed_message = parser.parse_message(message)
        if parsed_message is not None:
            parsed_messages.append(parsed_message)
    return parsed_messages

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
                logger.info(f'[CLIENT]: send message {id} to server')
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.post('http://localhost:8000/messages', json=parsed_message, headers=headers)
                await handle_response(client, response)
    except Exception as e:
        logger.error(f"[CLIENT]: Error when posting messages {e}")
        
async def authenticate_user(user: User, client):
    """
    Authenticates a user with the API server.
    
    Args:
        user (dict): User information including username and password.
        client: An asynchronous client for making requests.
    
    Returns:
        str: Authentication token if authentication is successful.
    
    Notes:
        This function signs up and logs in a user, obtaining an authentication token from the server.
        Logs information about the process.
    """
    try:
        username = user["username"]
        resp = await client.post('http://localhost:8000/users', json=user)
        if resp.status_code == 201:
            logger.info(f"[CLIENT]: {username} has signup")
        resp = await client.post('http://localhost:8000/users/login', json=user)
        if resp.status_code == 201:
            logger.info(f"[CLIENT]: {username} has logged in")    
        token = resp.json()["token"]
        return token
    except Exception as e:
        logger.error(f"[CLIENT]: Error when auth user in API {e}")      
          
async def run(scraper: Scraper, parser: MessageParser, user: User):
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
