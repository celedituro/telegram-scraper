import psycopg2
from psycopg2 import IntegrityError

class Database:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
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
            print("[DATABASE]: Error when connecting to db:", e)

    def create_messages_table(self):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER, content TEXT NOT NULL, date DATE, type TEXT NOT NULL)"
            cursor.execute(sql_sentence)
            self.connection.commit()
            cursor.close()
            print("[DATABASE]: messages table created")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when creating messages table:", e)

    def create_users_table(self):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)"
            cursor.execute(sql_sentence)
            self.connection.commit()
            cursor.close()
            print("[DATABASE]: users table created")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when creating users table:", e)
    
    def create_tables(self):
        try:
            self.create_messages_table()
            self.create_users_table()
        except psycopg2.Error as e:
            print("[DATABASE]: Error when creating tables:", e)

    def close(self):
        self.connection.close()
        print("[DATABASE]: db disconnected")


