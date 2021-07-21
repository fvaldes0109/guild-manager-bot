import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telepot

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Has iniciado el bot")

def help(update, context):
    update.message.reply_text("Esta es la ayuda")

def echo(update, context):
    update.message.reply_text("No entendi :v")

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""

bot = telepot.Bot(os.environ['TOKEN'])
updater = Updater(os.environ['TOKEN'], use_context = True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))

#On non command...
dp.add_handler(MessageHandler(Filters.text, echo))

#Log all errors
dp.add_error_handler(error)

#Start the bot
updater.start_polling()

#Run the bot until you press Ctrl+C
updater.idle()

if __name__ == '__main__':
    main()