class MessageService:
    def __init__(self, database):
        self.database = database

    def add_message(self, message):
        self.database.insert_message(message)

    def get_all_messages(self):
        return self.database.get_all_messages()


