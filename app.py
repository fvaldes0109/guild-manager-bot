import logging
import os
import mysql.connector
import texts

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telepot

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(texts.start)

def help(update, context):
    update.message.reply_text(texts.help)

def echo(update, context):
    update.message.reply_text("No entendi :v")

def main():
    """Start the bot."""

mydb = mysql.connector.connect(
    host = os.environ['dbhost'],
    user = os.environ['dbuser'],
    password = os.environ['dbpassword'],
    database = os.environ['dbname']
)

bot = telepot.Bot(os.environ['TOKEN'])
updater = Updater(os.environ['TOKEN'], use_context = True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))

#On non command...
dp.add_handler(MessageHandler(Filters.text, echo))

#Start the bot
updater.start_polling()

#Run the bot until you press Ctrl+C
updater.idle()

if __name__ == '__main__':
    main()