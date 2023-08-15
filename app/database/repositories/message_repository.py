import psycopg2
from loguru import logger
from datetime import date

from ..database import Database

class MessageRepository:
    """
    A class responsible for managing database operations related to messages.

    Args:
        database (Database): An instance of the Database class representing the database connection.

    Attributes:
        db (Database): The database connection instance.

    Methods:
        get_all_messages(): Retrieves all messages from the database.
        insert_message(id: int, channel_id: int, content: str, date: date, message_type: str): Inserts a message into the database.
        get_link_messages(): Retrieves all link messages from the database.
        get_message(id: int): Retrieves a specific message by ID from the database.

    Notes:
        This class manages database interactions for messages, including retrieval, insertion, and querying.
    """
    
    def __init__(self, database: Database):
        """
        Initializes the MessageRepository class with a database connection instance.

        Args:
            database (Database): An instance of the Database class representing the database connection.
        """
        self.db = database
    
    def get_all_messages(self):
        """
        Retrieves all messages from the database.

        Returns:
            list: A list of tuples representing all messages in the database.

        Notes:
            This method queries the database for all messages and returns them as a list of tuples.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM messages"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            logger.info("[MESSAGE REPOSITORY]: got all messages")
            return messages
        except psycopg2.Error as e:
            logger.error(f"[MESSAGE REPOSITORY]: Error when getting all messages - {e}")
            
    def insert_message(self, id: int, channel_id: int, content: str, date: date, message_type: str):
        """
        Inserts a message into the database.

        Args:
            id (int): The message ID.
            channel_id (int): The channel ID.
            content (str): The message content.
            date (date): The message date.
            message_type (str): The message type.

        Returns:
            tuple: The inserted message information.

        Notes:
            This method inserts a message into the 'messages' table and returns the inserted message information as a tuple.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "INSERT INTO messages (id, channel_id, content, date, type) VALUES (%s, %s, %s, %s, %s) RETURNING *"
            cursor.execute(sql_sentence, (id, channel_id, content, date, message_type))
            inserted_message = cursor.fetchone()
            self.db.connection.commit()
            cursor.close()
            logger.info(f"[MESSAGE REPOSITORY]: message {id} was added")
            return inserted_message
        except psycopg2.Error as e:
            logger.error(f"[MESSAGE REPOSITORY]: Error when inserting message {id} - {e}")
            
    def get_link_messages(self):
        """
        Retrieves all link messages from the database.

        Returns:
            list: A list of tuples representing link messages in the database.

        Notes:
            This method queries the database for all link messages and returns them as a list of tuples.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM messages WHERE type = 'link'"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            logger.info("[MESSAGE REPOSITORY]: got link messages")
            return messages
        except psycopg2.Error as e:
            logger.error("[MESSAGE REPOSITORY]: Error when getting link messages - {e}")
    
    def get_message(self, id: int):
        """
        Retrieves a specific message by ID from the database.

        Args:
            id (int): The message ID.

        Returns:
            tuple: The retrieved message information.

        Notes:
            This method queries the database for a specific message by ID and returns its information as a tuple.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM messages WHERE id = %s"
            cursor.execute(sql_sentence, (id,))
            message = cursor.fetchone()
            cursor.close()
            logger.info(f"[MESSAGE REPOSITORY]: got message with id {id}")
            return message
        except psycopg2.Error as e:
            logger.error(f"[MESSAGE REPOSITORY]: Error when getting message {id} - {e}")