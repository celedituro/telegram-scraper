import psycopg2
from psycopg2 import IntegrityError

from ..database import Database

class UserRepository:
    def __init__(self, database: Database):
        self.db = database
            
    def insert_user(self, username, password):
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING *"
            cursor.execute(sql_sentence, (username, password))
            inserted_message = cursor.fetchone()
            self.db.connection.commit()
            cursor.close()
            return inserted_message
            print(f"[USER REPOSITORY]: user {username} was added")
        except IntegrityError as e:
            raise IntegrityError(e)
        except psycopg2.Error as e:
            print(f"[USER REPOSITORY]: Error when inserting user {username}:", e)