from pydantic import BaseModel

class Message(BaseModel):
    id: int
    channel_id: int
    content: str
    date: str