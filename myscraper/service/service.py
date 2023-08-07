from datetime import datetime

def parse_date(date_str, format):
    date_datetime = datetime.strptime(date_str, format)
    return date_datetime.date()
    
class MessageService:
    def __init__(self, database):
        self.database = database

    def add_message(self, id, channel_id, content, date, message_type):
        print(f'[MESSAGE SERVICE]: adding message: ({id}, {channel_id}, {content}, {date}, {message_type.name})')
        self.database.insert_message(id, channel_id, content, parse_date(date, '%Y-%m-%d'), message_type.name)

    def get_all_messages(self):
        print('[MESSAGE SERVICE]: getting all messages')
        return self.database.get_all_messages()

    def get_link_messages(self):
        print('[MESSAGE SERVICE]: getting link messages')
        return self.database.get_link_messages()


