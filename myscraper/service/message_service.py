class MessageService:
    def __init__(self, database):
        self.database = database

    def add_message(self, id, content):
        print(f'[MESSAGE SERVICE]: adding message: ({id}, {content})')
        self.database.insert_message(id, content)

    def get_all_messages(self):
        print('[MESSAGE SERVICE]: getting all messages')
        return self.database.get_all_messages()


