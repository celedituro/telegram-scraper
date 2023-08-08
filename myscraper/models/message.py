from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    text = "text"
    photo = "photo"
    link = "link"
    
class Message(BaseModel):
    id: int
    channel_id: int
    content: str
    date: str
    message_type: MessageType

class LinkMessage(BaseModel):
    id: int
    channel_id: int
    content: str
    date: str