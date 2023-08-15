import asyncio
import os

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from dotenv import load_dotenv
from psycopg2 import IntegrityError

from .services.message_service import MessageService
from .services.user_service import UserService
from .services.auth_service import AuthService
from .models.message_presenter import MessagePresenter
from .models.user_presenter import UserPresenter
from .models.encrypter import Encrypter
from .models.data_models import Message, LinkMessage, User, UserSignupResponse, UserLoginResponse
from .exceptions.message_exceptions import MessageAlreadyExist
from .exceptions.user_exceptions import UserNotFound, UserAlreadyExist, IncorrectPassword, InvalidPassword
from .exceptions.auth_exceptions import ExpiredToken, InvalidToken
from .database.database import Database
from .database.repositories.message_repository import MessageRepository
from .database.repositories.user_respository import UserRepository
from .utils.responses import create_message_responses, get_messages_responses, create_user_responses, login_user_responses

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

# Create an instance of HTTPBearer to handle the authentication header
bearer = HTTPBearer()

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

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        user = auth_service.decodeJWT(credentials.credentials)
        return user
    except InvalidToken as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    except ExpiredToken as e:
        raise HTTPException(status_code=401, detail="Expired Token")

@app.get('/', status_code=200)
def read_root():
    return {'Welcome to the Telegram Channels Scraper'}

@app.post("/messages", status_code=201, response_model=Message, responses=create_message_responses)
def add_message(message: Message, username: str = Depends(verify_token)):
    """
    Create a new message.
    """
    try:
        return message_service.add_message(message)
    except InvalidToken as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    except ExpiredToken as e:
        raise HTTPException(status_code=401, detail="Expired Token")
    except MessageAlreadyExist:
        raise HTTPException(status_code=400, detail="Message Already Exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new message: ' + str(e))

@app.get("/messages", status_code=200, response_model=List[Message], responses=get_messages_responses)
def get_all_messages(username: str = Depends(verify_token)):
    """
    Get a list of messages.
    """
    try:
        return message_service.get_all_messages()
    except InvalidToken as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    except ExpiredToken as e:
        raise HTTPException(status_code=401, detail="Expired Token")
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting messages: ' + str(e))

@app.get("/messages/link", status_code=200, response_model=List[LinkMessage], responses=get_messages_responses)
def get_link_messages(username: str = Depends(verify_token)):
    """
    Get a list of link messages.
    """
    try:
        return message_service.get_link_messages()
    except InvalidToken as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
    except ExpiredToken as e:
        raise HTTPException(status_code=401, detail="Expired Token")
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in getting link messages: ' + str(e))

@app.post("/users", status_code=201, response_model=UserSignupResponse, responses=create_user_responses)
def add_user(user: User):
    """
    Create a new user.
    """
    try:
        return user_service.add_user(user)
    except InvalidPassword:
        raise HTTPException(status_code=404, detail="Invalid password")
    except UserAlreadyExist:
        raise HTTPException(status_code=400, detail="User Already Exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when adding new user: ' + str(e))

@app.post("/users/login", status_code=201, response_model=UserLoginResponse, responses=login_user_responses)
def add_user(user: User):
    """
    Create a user's login session.
    """
    try:
        if user_service.login_user(user) is not None:
            token = auth_service.getJWT(user.username)
            return user_service.presenter.present_user_token(token)
    except IncorrectPassword:
        raise HTTPException(status_code=400, detail='Incorrect Password')
    except UserNotFound:
        raise HTTPException(status_code=404, detail='User Not Found')
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error when logging user: ' + str(e))