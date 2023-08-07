from datetime import datetime

def parse_date(date_str, format):
    date_datetime = datetime.strptime(date_str, format)
    return date_datetime.date()
    
class MessageService:
    def __init__(self, database):
        self.database = database

    def add_message(self, id, channel_id, content, date):
        print(f'[MESSAGE SERVICE]: adding message: ({id}, {channel_id}, {content}, {date})')
        self.database.insert_message(id, channel_id, content, parse_date(date, '%Y-%m-%d'))

    def get_all_messages(self):
        print('[MESSAGE SERVICE]: getting all messages')
        return self.database.get_all_messages()


