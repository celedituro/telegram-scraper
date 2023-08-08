import psycopg2

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

    def create_message_table(self):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, channel_id INTEGER, content TEXT NOT NULL, date DATE, type TEXT NOT NULL)"
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
            
    async def insert_message(self, id, channel_id, content, date, message_type):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "INSERT INTO messages (id, channel_id, content, date, type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_sentence, (id, channel_id, content, date, message_type))
            self.connection.commit()
            cursor.close()
            print(f"[DATABASE]: message {id} was added")
        except psycopg2.Error as e:
            print(f"[DATABASE]: Error when inserting message {id}:", e)
            
    def get_link_messages(self):
        try:
            cursor = self.connection.cursor()
            sql_sentence = "SELECT * FROM messages WHERE type = 'link'"
            cursor.execute(sql_sentence)
            messages = cursor.fetchall()
            cursor.close()
            return messages
            print("[DATABASE]: got link messages")
        except psycopg2.Error as e:
            print("[DATABASE]: Error when getting link messages:", e)

    def close(self):
        self.connection.close()
        print("[DATABASE]: db disconnected")


