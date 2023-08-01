from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
bot_token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')
chat_name = os.environ.get('CHAT_NAME')

class TelegramBot:
    def __init__(self):
        print("Telegram init")
        self.updater = Updater(bot_token)
        dispatcher = self.updater.dispatcher

        # Define commands that the bot understand
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("get_messages", self.get_messages))
    
    def start_bot(self):
        print("Telegram bot listening")
        self.updater.start_polling()
    
    # Response to /start    
    def start(self, update: Update, _: CallbackContext) -> None:
        print("Telegram bot get /start")
        update.message.reply_text("¡Hola! Soy tu bot para extraer mensajes de un canal de Telegram. Envíame el comando /get_messages para obtener los mensajes del canal.")

    # Response to /get_messages    
    def get_messages(self, update: Update, context: CallbackContext) -> None:
        print("Telegram bot get /get_messages")
        try:
            id = update.message.chat_id
            messages = context.bot.get_chat_history(id)
            print("Get:", messages)

            for message in messages:
                update.message.reply_text(message.text)
                
        except Exception as e:
            update.message.reply_text(f"Ha ocurrido un error, intente más tarde: {e}")


