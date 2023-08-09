import psycopg2
from psycopg2 import IntegrityError

from ..database import Database

class MessageRepository:
    def __init__(self, database: Database):
        self.db = database
    
    def get_all_messages(self):
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM messages"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            return messages
            print("[MESSAGE REPOSITORY]: got all messages")
        except psycopg2.Error as e:
            print("[MESSAGE REPOSITORY]: Error when getting all messages:", e)
            
    def insert_message(self, id, channel_id, content, date, message_type):
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "INSERT INTO messages (id, channel_id, content, date, type) VALUES (%s, %s, %s, %s, %s) RETURNING *"
            cursor.execute(sql_sentence, (id, channel_id, content, date, message_type))
            inserted_message = cursor.fetchone()
            self.db.connection.commit()
            cursor.close()
            return inserted_message
            print(f"[MESSAGE REPOSITORY]: message {id} was added")
        except IntegrityError as e:
            raise IntegrityError(e)
        except psycopg2.Error as e:
            print(f"[MESSAGE REPOSITORY]: Error when inserting message {id}:", e)
            
    def get_link_messages(self):
        try:
            cursor = self.db.connection.cursor()
            sql_sentence = "SELECT * FROM messages WHERE type = 'link'"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            return messages
            print("[MESSAGE REPOSITORY]: got link messages")
        except psycopg2.Error as e:
            print("[MESSAGE REPOSITORY]: Error when getting link messages:", e)