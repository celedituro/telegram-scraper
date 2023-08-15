from pydantic import BaseModel
from enum import Enum
from datetime import date

class MessageType(str, Enum):
    text = "text"
    photo = "photo"
    link = "link"
    
class Message(BaseModel):
    id: int
    channel_id: int
    content: str
    date: date
    message_type: MessageType

class LinkMessage(BaseModel):
    id: int
    channel_id: int
    content: str
    date: date
        
class User(BaseModel):
    username: str
    password: str
    
class UserSignupResponse(BaseModel):
    username: str
    hashed_password: str
    
class UserLoginResponse(BaseModel):
    token: str