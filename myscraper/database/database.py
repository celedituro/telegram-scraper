import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')

class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            print("[DATABASE]: db connected")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when connecting to database:", e)

    def create_message_table(self):
        try:
            cursor = self.connection.cursor()
            #sql_sentence = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER NOT NULL, content TEXT NOT NULL, date DATE NOT NULL)"
            sql_sentence = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER, content TEXT NOT NULL)"
            cursor.execute(sql_sentence)
            self.connection.commit()
            cursor.close()
            print("[DATABASE]: messages table created")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when creating messages table:", e)
    
    def get_all_messages(self):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "SELECT * FROM messages"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            return messages
            print("[DATABASE]: got all messages")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when getting all messages:", e)
            
    def insert_message(self, id, channel_id, content):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "INSERT INTO messages (id, channel_id, content) VALUES (%s, %s, %s)"
            cursor.execute(sql_sentence, (id, channel_id, content))
            self.connection.commit()
            cursor.close()
            print(f"[DATABASE]: message {id} was added")
        except psycopg2.Error as e:
            print(f"[DATABASE]: Error when inserting message {id}:", e)

    def close(self):
        self.connection.close()
        print("[DATABASE]: db disconnected")


