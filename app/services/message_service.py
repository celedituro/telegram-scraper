from datetime import datetime

from ..exceptions.message_exceptions import MessageAlreadyExist
from ..database.repositories.message_repository import MessageRepository
from ..models.message_presenter import MessagePresenter
from ..models.data_models import Message

class MessageService:
    """
    A class responsible for managing operations related to messages.

    Args:
        repository (MessageRepository): An instance of the MessageRepository class for database operations.
        presenter (MessagePresenter): An instance of the MessagePresenter class for data presentation.

    Attributes:
        repository (MessageRepository): The message repository instance.
        presenter (MessagePresenter): The message presenter instance.

    Methods:
        add_message(message: Message): Adds a message to the database.
        get_all_messages(): Retrieves all messages from the database.
        get_link_messages(): Retrieves all link messages from the database.

    Notes:
        This class provides methods to manage messages, including addition and retrieval.
    """
    
    def __init__(self, repository: MessageRepository, presenter: MessagePresenter):
        """
        Initializes the MessageService class with a message repository and presenter.

        Args:
            repository (MessageRepository): An instance of the MessageRepository class for database operations.
            presenter (MessagePresenter): An instance of the MessagePresenter class for data presentation.
        """
        self.repository = repository
        self.presenter = presenter

    def add_message(self, message: Message):
        """
        Adds a message to the database.

        Args:
            message (Message): The message to be added.

        Returns:
            dict: The added message information.

        Raises:
            MessageAlreadyExist: If the message already exists in the database.

        Notes:
            This method checks if the message already exists. If not, it inserts the message into the database
            and returns the added message information. Otherwise, it raises an exception.
        """
        if self.repository.get_message(message.id) is None:
            new_message = self.repository.insert_message(message.id, message.channel_id, message.content, message.date, message.message_type.name)
            return self.presenter.present_message(new_message)
        raise MessageAlreadyExist("The message already exist")

    def get_all_messages(self):
        """
        Retrieves all messages from the database.

        Returns:
            list: A list of dictionaries representing all messages.

        Notes:
            This method retrieves all messages from the database and presents them using the message presenter.
        """
        messages = self.repository.get_all_messages()
        return self.presenter.present_all_messages(messages)

    def get_link_messages(self):
        """
        Retrieves all link messages from the database.

        Returns:
            list: A list of dictionaries representing link messages.

        Notes:
            This method retrieves all link messages from the database and presents them using the message presenter.
        """
        link_messages = self.repository.get_link_messages()
        return self.presenter.present_link_messages(link_messages)


