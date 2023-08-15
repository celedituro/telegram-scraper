import base64
from datetime import datetime
from telethon.tl.types import InputMessagesFilterEmpty, MessageMediaPhoto, MessageMediaWebPage

from api.models.data_models import MessageType

class MessageParser:
    """
    A class responsible for parsing and formatting Telegram messages.

    Attributes:
        media_handlers (dict): A dictionary mapping message media types to corresponding handling methods.

    Methods:
        get_photo_content(media): Retrieves base64-encoded content of a photo message.
        get_webpage_content(media): Retrieves the URL of a web page message.
        get_message_date(date: datetime, format): Formats a message date.
        get_message_content(message): Retrieves formatted message content.
        get_message_type(message): Determines the type of a message.
        parse_message(message): Parses and formats a Telegram message.

    Notes:
        This class assists in parsing and presenting different types of Telegram messages.
    """
    
    def __init__(self):
        """
        Initializes the MessageParser with media handling methods.
        """
        self.media_handlers = {
            MessageMediaPhoto: self.get_photo_content,
            MessageMediaWebPage: self.get_webpage_content
        }
    
    def get_photo_content(self, media):
        """
        Retrieves base64-encoded content of a photo message.

        Args:
            media (MessageMediaPhoto): The media object representing the photo.

        Returns:
            str: Base64-encoded content of the photo.
        """
        return base64.b64encode(media.photo.sizes[0].bytes).decode('utf-8')
    
    def get_webpage_content(self, media):
        """
        Retrieves the URL of a web page message.

        Args:
            media (MessageMediaWebPage): The media object representing the web page.

        Returns:
            str: The URL of the web page.
        """
        return media.webpage.url
    
    def get_message_date(self, date: datetime, format):
        """
        Formats a message date.

        Args:
            date (datetime): The message date.
            format (str): The desired date format.

        Returns:
            str: The formatted date string.
        """
        return date.strftime(format)

    def get_message_content(self, message):
        """
        Retrieves formatted message content.

        Args:
            message: The Telegram message.

        Returns:
            str: The formatted message content.
        """
        media_handler = self.media_handlers.get(type(message.media))
        if media_handler:
            return media_handler(message.media)
        return message.message
    
    def get_message_type(self, message):
        """
        Parses and formats a Telegram message.

        Args:
            message: The Telegram message.

        Returns:
            dict: The parsed and formatted message.
        """
        media_type = type(message.media) if message.media else None
        return {
            MessageMediaPhoto: MessageType.photo,
            MessageMediaWebPage: MessageType.link
        }.get(media_type, MessageType.text)
           
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