from datetime import datetime
    
class MessageService:
    def __init__(self, message_repository, presenter):
        self.message_repository = message_repository
        self.presenter = presenter

    def add_message(self, message):
        new_message = self.message_repository.insert_message(message.id, message.channel_id, message.content, message.date, message.message_type.name)
        return self.presenter.present_message(new_message)

    def get_all_messages(self):
        messages = self.message_repository.get_all_messages()
        return self.presenter.present_all_messages(messages)

    def get_link_messages(self):
        link_messages = self.message_repository.get_link_messages()
        return self.presenter.present_link_messages(link_messages)


