import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import List
from psycopg2 import IntegrityError

from ..services.message_service import MessageService
from ..services.user_service import UserService
from ..services.auth_service import AuthService
from ..models.message_presenter import MessagePresenter
from ..models.user_presenter import UserPresenter
from ..models.encrypter import Encrypter
from ..models.message import Message, LinkMessage
from ..models.user import User, UserSignupResponse, UserLoginResponse
from ..models.exceptions import UserNotFound
from ..database.database import Database
from ..database.repositories.message_repository import MessageRepository
from ..database.repositories.user_respository import UserRepository
from ..utils.swagger_responses import message_post_responses, get_responses, user_signup_responses, user_login_responses

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

app = FastAPI()

# Add the middleware of CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
db.create_tables()

message_repository = MessageRepository(db)
user_repository = UserRepository(db)

message_presenter = MessagePresenter()
message_service = MessageService(message_repository, message_presenter)
encrypter = Encrypter()
user_presenter = UserPresenter()
auth_service = AuthService()
user_service = UserService(user_repository, encrypter, user_presenter)

@app.get('/', status_code=200)
def read_root():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/messages", status_code=201, response_model=Message, responses=message_post_responses)
def add_message(message: Message):
    """
    Create a new message.
    """
    try:
        return message_service.add_message(message)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Message already exists", headers={"X-Error": "ItemDuplicate"})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200, response_model=List[Message], responses=get_responses)
def get_all_messages():
    """
    Get a list of messages.
    """
    try:
        return message_service.get_all_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))

@app.get("/messages/link", status_code=200, response_model=List[LinkMessage], responses=get_responses)
def get_link_messages():
    """
    Get a list of link messages.
    """
    try:
        return message_service.get_link_messages()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting link messages: ' + str(e))

@app.post("/users/signup", status_code=201, response_model=UserSignupResponse, responses=user_signup_responses)
def add_user(user: User):
    """
    Create a new user.
    """
    try:
        return user_service.add_user(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists", headers={"X-Error": "ItemDuplicate"})
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new user: ' + str(e))

@app.post("/users/login", status_code=201, response_model=UserLoginResponse, responses=user_login_responses)
def add_user(user: User):
    """
    Create a user's login session.
    """
    try:
        if user_service.login_user(user):
            token = auth_service.getJWT(user.username)
            return { "token": token }
        raise UserNotFound('the user does not exist')
    except UserNotFound:
        raise HTTPException(status_code=404, detail='the user does not exist')
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when logging user: ' + str(e))