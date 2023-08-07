from pydantic import BaseModel
import datetime

class Message(BaseModel):
    id: int
    channel_id: int
    content: str
    #date: datetime.datetime