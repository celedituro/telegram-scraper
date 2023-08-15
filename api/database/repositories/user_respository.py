import psycopg2
from loguru import logger

from ..database import Database

class UserRepository:
    """
    A class responsible for managing database operations related to users.

    Args:
        database (Database): An instance of the Database class representing the database connection.

    Attributes:
        db (Database): The database connection instance.

    Methods:
        insert_user(username: str, password: str): Inserts a user into the database.
        get_user(username: str): Retrieves a user by username from the database.

    Notes:
        This class manages database interactions for users, including insertion and retrieval.
    """
    
    def __init__(self, database: Database):
        """
        Initializes the UserRepository class with a database connection instance.

        Args:
            database (Database): An instance of the Database class representing the database connection.
        """
        self.db = database
            
    def insert_user(self, username: str, password: str):
        """
        Inserts a user into the database.

        Args:
            username (str): The username of the user.
            password (str): The encrypted password of the user.

        Returns:
            tuple: The inserted user information.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_sentence, (username, password))
            inserted_message = cursor.fetchone()
            self.db.connection.commit()
            cursor.close()
            logger.info(f"[USER REPOSITORY]: user {username} was added")
            return inserted_message
        except psycopg2.Error as e:
            logger.error(f"[USER REPOSITORY]: Error when inserting user {username} - {e}")
    
    def get_user(self, username: str):
        """
        Retrieves a user by username from the database.

        Args:
            username (str): The username of the user.

        Returns:
            tuple: The retrieved user information.
        """
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql_sentence, (username,))
            user = cursor.fetchone()
            cursor.close()
            logger.info(f"[USER REPOSITORY]: got user with username {username}")
            return user
        except psycopg2.Error as e:
            logger.error(f"[USER REPOSITORY]: Error when getting user {username} - {e}")
            