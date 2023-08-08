from telethon.tl.types import InputMessagesFilterEmpty, MessageMediaPhoto, MessageMediaWebPage
import base64
from datetime import datetime
from .message import MessageType

class MessageParser:
    def get_photo_content(self, photo_bytes):
        return base64.b64encode(photo_bytes).decode('utf-8')
    
    def get_message_date(self, date, format):
        return date.strftime(format)

    def get_message_content(self, message):
        content = message.message
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                content = self.get_photo_content(message.media.photo.sizes[0].bytes)
            if isinstance(message.media, MessageMediaWebPage):
                content = message.media.webpage.url
                
        return content
    
    def get_message_type(self, message):
        message_type = MessageType.text
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                message_type = MessageType.photo
            if isinstance(message.media, MessageMediaWebPage):
                message_type = MessageType.link
        return message_type
    
    def parse_date(self, date_str):
        date_datetime = datetime.strptime(date_str, '%Y-%m-%d')
        return date_datetime.date()
            
    def parse_message(self, message):
        # Ignore MessageService messages
        if message.message or message.media:
            msg = {
                "id": message.id,
                "channel_id": message.peer_id.channel_id,
                "content": self.get_message_content(message),
                "date": self.get_message_date(message.date, '%Y-%m-%d'),
                "message_type": self.get_message_type(message)
            }
            return msg