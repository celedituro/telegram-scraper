import psycopg2
from loguru import logger

class Database:
    def __init__(self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
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
        try:
            self.create_messages_table()
            self.create_users_table()
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when creating tables:", e)

    def close(self):
        try:
            self.connection.close()
            logger.info("[DATABASE]: db disconnected")
        except psycopg2.Error as e:
            logger.error("[DATABASE]: Error when disconnecting db", e)


