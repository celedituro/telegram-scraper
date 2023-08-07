from telethon.tl.types import InputMessagesFilterEmpty, MessageMediaPhoto, MessageMediaWebPage

class MessageParser:        
    def get_message_content(self, message):
        content = message.message
        if message.media:
            if isinstance(message.media, MessageMediaPhoto):
                content = message.media.photo.sizes[0].bytes
            if isinstance(message.media, MessageMediaWebPage):
                content = message.media.webpage.url
                
        return content
        
    def parse_message(self, message):
        # Ignore MessageService messages
        if message.message:
            msg = {
                "id": message.id,
                "channel_id": message.peer_id.channel_id,
                "content": self.get_message_content(message),
                "date": message.date.strftime('%Y-%m-%d')
            }
            return msg
