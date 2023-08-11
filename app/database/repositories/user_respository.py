import psycopg2
from loguru import logger

from ..database import Database

class UserRepository:
    def __init__(self, database: Database):
        self.db = database
            
    def insert_user(self, username: str, password: str):
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
            