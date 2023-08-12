from datetime import datetime

from ..exceptions.message_exceptions import MessageAlreadyExist
from ..database.repositories.message_repository import MessageRepository
from ..models.message_presenter import MessagePresenter
from ..models.data_models import Message

class MessageService:
    def __init__(self, repository: MessageRepository, presenter: MessagePresenter):
        self.repository = repository
        self.presenter = presenter

    def add_message(self, message: Message):
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


