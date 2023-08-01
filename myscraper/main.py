from .database import Database
from .bot import TelegramBot
import threading
from .api import app
import uvicorn

def run_db():
    try:
        db = Database()
        db.create_message_table()
        # Perform other operations with the database if needed
    except Exception as e:
        print("Error during application execution:", e)
    finally:
        db.close()

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

bot = TelegramBot()

# Spawn bot thread
bot_thread = threading.Thread(target=bot.start_bot)
print("Spawn bot thread")
bot_thread.start()

# Spawn API thread
api_thread = threading.Thread(target=run_api)
print("Spawn api thread")
api_thread.start()

# Wait bot and API threads to join
bot_thread.join()
print("Bot thread finished")
api_thread.join()
print("Api thread finished")

