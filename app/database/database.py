import psycopg2
from loguru import logger

class Database:
    """
    A class responsible for managing database connections and operations.

    Args:
        db_name (str): The name of the database.
        db_user (str): The username for database authentication.
        db_password (str): The password for database authentication.
        db_host (str): The host address of the database server.
        db_port (str): The port number for database access.

    Attributes:
        connection: The database connection object.

    Methods:
        create_messages_table(): Creates the 'messages' table if it doesn't exist.
        create_users_table(): Creates the 'users' table if it doesn't exist.
        create_tables(): Creates both the 'messages' and 'users' tables.
        close(): Closes the database connection.
    """
    
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
        """
        Initializes the Database class and establishes a database connection.

        Args:
            db_name (str): The name of the database.
            db_user (str): The username for database authentication.
            db_password (str): The password for database authentication.
            db_host (str): The host address of the database server.
            db_port (str): The port number for database access.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            logger.info("[DATABASE]: db connected")
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when connecting to db:", e)

    def create_messages_table(self):
        """
        Creates the 'messages' table if it doesn't exist.
        """
        try:
            cursor = self.connection.cursor()
            sql_sentence = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER, content TEXT NOT NULL, date DATE, type TEXT NOT NULL)"
            cursor.execute(sql_sentence)
            self.connection.commit()
            cursor.close()
            logger.info("[DATABASE]: messages table created")
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when creating messages table:", e)

    def create_users_table(self):
        """
        Creates the 'users' table if it doesn't exist.
        """
        try:
            cursor = self.connection.cursor()
            sql_sentence = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)"
            cursor.execute(sql_sentence)
            self.connection.commit()
            cursor.close()
            logger.info("[DATABASE]: users table created")
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when creating users table:", e)
    
    def create_tables(self):
        """
        Creates both the 'messages' and 'users' tables.
        """
        try:
            self.create_messages_table()
            self.create_users_table()
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when creating tables:", e)

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.connection.close()
            logger.info("[DATABASE]: db disconnected")
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when disconnecting db", e)


