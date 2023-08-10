import asyncio
import os
import httpx

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
    username = input('Username:')
    password = input('Password:')
    user = {
        "username": username,
        "password": password
    }
    return user 

async def handle_response(client, response):
    if response.status_code == REDIRECTION_STATUS_CODE:
        new_location = response.headers.get('Location')
        print(f'[CLIENT]: redirecting request to: {new_location}')
        response = await client.post(new_location, json=data)
    print("[CLIENT]: receive from server:", response.status_code)
            
async def post_messages(client, messages, parser: MessageParser, token: str):
    try:
        for message in messages:
            parsed_message = parser.parse_message(message)
            if parsed_message:
                id = parsed_message["id"]
                print(f'[CLIENT]: send {id} to server')
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.post(f'{API_URL}/messages', json=parsed_message, headers=headers)
                await handle_response(client, response)
    except Exception as e:
        print("[CLIENT]: Error when posting messages", e)  
          
async def run(scraper: Scraper, parser: MessageParser, user: User):
    async with httpx.AsyncClient() as client:
        try:
            username = user["username"]
            resp = await client.post(f'{API_URL}/users', json=user)
            if resp.status_code == 201:
                print(f"{username} has signup")
            resp = await client.post(f'{API_URL}/users/login', json=user)
            if resp.status_code == 201:
                print(f"{username} has logged in")
            messages = await scraper.get_messages(PHONE_NUMBER, GROUP_USERNAME)
            token = resp.json()["token"]
            print("token:", token)
            await post_messages(client, messages, parser, token)
        except Exception as e:
            print("[CLIENT]: Error when running client", e)      
         
if __name__ == '__main__':
    user = get_user_credentials()
    print(user["username"])
    scraper = Scraper(API_ID, API_HASH)
    parser = MessageParser()
    asyncio.run(run(scraper, parser, user))
