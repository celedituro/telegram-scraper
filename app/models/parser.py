from telethon.tl.types import InputMessagesFilterEmpty, MessageMediaPhoto, MessageMediaWebPage
import base64
from datetime import datetime
from .data_models import MessageType

class MessageParser:
    """
    Creates an instance of the message parser.
    
    Returns:
        A message parser.
    """
    def __init__(self):
        self.media_handlers = {
            MessageMediaPhoto: self.get_photo_content,
            MessageMediaWebPage: self.get_webpage_content
        }
    
    """
    Gets the content of a photo message.
    
    Args:
        media: a telegram photo media.
        
    Returns:
        A string encoded with base64.
    """
    def get_photo_content(self, media):
        return base64.b64encode(media.photo.sizes[0].bytes).decode('utf-8')
    
    """
    Gets the content of a webpage message.
    
    Args:
        media: a telegram url media.
        
    Returns:
        A string.
    """
    def get_webpage_content(self, media):
        return media.webpage.url
    
    """
    Gets the message date in a given format.
    
    Args:
        date: datetime.
        format: datetime format.
        
    Returns:
        A date.
    """
    def get_message_date(self, date: datetime, format):
        return date.strftime(format)

    """
    Gets the content of the message depending if its a text, photo or link message.
    
    Args:
        message: Message object from Telegram.
        
    Returns:
        A string.
    """
    def get_message_content(self, message):
        media_handler = self.media_handlers.get(type(message.media))
        if media_handler:
            return media_handler(message.media)
        return message.message
    
    """
    Gets the message type of the message.
    
    Args:
        message: Message object from Telegram.
        
    Returns:
        An instance of MessageType.
    """
    def get_message_type(self, message):
        media_type = type(message.media) if message.media else None
        return {
            MessageMediaPhoto: MessageType.photo,
            MessageMediaWebPage: MessageType.link
        }.get(media_type, MessageType.text)
    
    """
    Parses a message received from Telegram into a Message type.
    
    Args:
        message: Message object from Telegram.
        
    Returns:
        A dictionary with id, channel_id, content, date and message_type.
    """        
    def parse_message(self, message):
        # ignore MessageService messages
        if message.message or message.media:
            msg = {
                "id": message.id,
                "channel_id": message.peer_id.channel_id,
                "content": self.get_message_content(message),
                "date": self.get_message_date(message.date, '%Y-%m-%d'),
                "message_type": self.get_message_type(message)
            }
            return msg