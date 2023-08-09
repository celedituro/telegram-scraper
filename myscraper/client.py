import asyncio
import os
from dotenv import load_dotenv
from models.parser import MessageParser
from models.scraper import Scraper

load_dotenv()
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROUP_USERNAME = os.environ.get('GROUP_USERNAME')

if __name__ == '__main__':
    scraper = Scraper(API_ID, API_HASH)
    parser = MessageParser()
    asyncio.run(scraper.run(parser, PHONE_NUMBER, GROUP_USERNAME))
