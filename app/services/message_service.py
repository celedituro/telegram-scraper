from datetime import datetime

from ..models.exceptions import MessageAlreadyExist

class MessageService:
    def __init__(self, repository, presenter):
        self.repository = repository
        self.presenter = presenter

    def add_message(self, message):
        if self.repository.get_message(message.id) is None:
            new_message = self.repository.insert_message(message.id, message.channel_id, message.content, message.date, message.message_type.name)
            return self.presenter.present_message(new_message)
        raise MessageAlreadyExist("The message already exist")

    def get_all_messages(self):
        messages = self.repository.get_all_messages()
        return self.presenter.present_all_messages(messages)

    def get_link_messages(self):
        link_messages = self.repository.get_link_messages()
        return self.presenter.present_link_messages(link_messages)

