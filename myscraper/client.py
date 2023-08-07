import asyncio
import os
from dotenv import load_dotenv
from models.parser import MessageParser
from models.scraper import Scraper

load_dotenv()
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
group_username = os.environ.get('GROUP_USERNAME')
api_url = os.environ.get('API_URL')

if __name__ == '__main__':
    scraper = Scraper(api_id, api_hash)
    parser = MessageParser()
    asyncio.run(scraper.run(parser, phone_number, group_username, api_url))
