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
            print(f"[USER REPOSITORY]: user {username} was added")
            return inserted_message
        except IntegrityError as e:
            raise IntegrityError(e)
        except psycopg2.Error as e:
            print(f"[USER REPOSITORY]: Error when inserting user {username}:", e)
    
    def get_user(self, username):
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql_sentence, (username,))
            user = cursor.fetchone()
            cursor.close()
            print(f"[USER REPOSITORY]: user with username {username} got")
            return user
        except IntegrityError as e:
            raise IntegrityError(e)
        except psycopg2.Error as e:
            print(f"[USER REPOSITORY]: Error when getting user {username}:", e)
            