import logging
import os
from modules import db_func, texts, date_check

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telepot

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(texts.start)

def help(update, context):
    update.message.reply_text(texts.help)

def echo(update, context):
    chat_id = update.message.chat_id
    if chat_id > 0: #If is in PM
        msg = update.message.text
        #Check if its forwarded from CWbot
        if update.message.forward_from != None and update.message.forward_from.username == 'chtwrsbot':
            if "Battle of the seven castles in" in msg: #Its a /me
                if date_check.isRecent(update.message.forward_date) == True: #Its from less than 2 minutes ago
                    db_func.addPlayer(chat_id, msg) #Add player to database
            
def main():
    """Start the bot."""

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