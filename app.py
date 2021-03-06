import logging
import os
import emoji
from modules import db_func, texts, date_check

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telepot

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(texts.start)

def help(update, context):
    update.message.reply_text(texts.help)

def reports(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    attendance = db_func.getAttendance(user_id)
    msg = texts.attendance(attendance[0], attendance[1], date_check.getBattleCount())
    bot.sendMessage(chat_id, msg, parse_mode = "HTML")

def reports_exp(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    exp = db_func.getExp(user_id)
    msg = texts.expReports(exp[0], exp[1])
    bot.sendMessage(chat_id, msg, parse_mode = "HTML")

def reports_gold(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    gold = db_func.getGold(user_id)
    msg = texts.goldReports(gold[0], gold[1])
    bot.sendMessage(chat_id, msg, parse_mode = "HTML")

def forays_stopped(update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    forays = db_func.getForays(user_id)
    msg = texts.forayReports(forays[0], forays[1])
    bot.sendMessage(chat_id, msg, parse_mode = "HTML")

def send_message(update, context):
    spl = update.message.text.split(' ')
    destiny_id = spl[1]
    text = spl[2:]
    result = ' '.join(text)
    bot.sendMessage(destiny_id, result)

def echo(update, context):
    if update.channel_post == None:
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        msg = update.message.text
        #Check if its forwarded from CWbot
        if update.message.forward_from != None and update.message.forward_from.username == 'chtwrsbot':
            if "Your result on the battlefield:" in msg and "Encounter:" not in msg: #Its a /report
                battleDate = date_check.getBattleDate(update.message.forward_date)
                if date_check.belongsToWeek(battleDate): #Si no es un reporte antiguo
                    result = db_func.addReport(user_id, msg, battleDate)
                    if result == True:
                        bot.sendMessage(user_id, emoji.emojize(":check_mark_button:Reporte contabilizado con ??xito!"))
                else:
                    bot.sendMessage(user_id, emoji.emojize(":cross_mark:Este reporte es muy antiguo"))
            elif "You lift up your sword" in msg: #Es un intervene atrapado
                intDate = date_check.getIntDate(update.message.forward_date) #Coge la fecha del intervene
                if date_check.belongsToWeek(intDate): #Si no es antiguo
                    db_func.addInt(user_id, intDate)
            if chat_id > 0: #If is in PM
                if "Battle of the seven castles in" in msg: #Its a /me
                    if date_check.isRecent(update.message.forward_date) == True: #Its from less than 2 minutes ag0 
                        db_func.addPlayer(user_id, msg) #Add player to database
                        bot.sendMessage(user_id, "Registrado con ??xito!")
                    else:
                        bot.sendMessage(user_id, "Este /me es muy antiguo. Por favor env??a otro")

def sendWeekReport():
    user_id = os.environ['tempuserid']
    attData = db_func.getAttendance(user_id)
    expData = db_func.getExp(user_id)
    goldData = db_func.getGold(user_id)
    forayData = db_func.getForays(user_id)
    msg = emoji.emojize(":snake::snake:<b><u>REPORTE SEMANAL DE [" + attData[0] + "]</u></b>:snake::snake:\n\n")
    msg = msg + texts.attendance(attData[0], attData[1], date_check.getBattleCount()) + "\n\n"
    msg = msg + texts.expReports(expData[0], expData[1]) + "\n\n"
    msg = msg + texts.goldReports(goldData[0], goldData[1]) + "\n\n"
    msg = msg + texts.forayReports(forayData[0], forayData[1])
    bot.sendMessage(os.environ['tempchannelid'], msg, parse_mode = "HTML")

date_check.startTimers(sendWeekReport)

bot = telepot.Bot(os.environ['TOKEN'])
updater = Updater(os.environ['TOKEN'], use_context = True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("reports", reports))
dp.add_handler(CommandHandler("reports_exp", reports_exp))
dp.add_handler(CommandHandler("reports_gold", reports_gold))
dp.add_handler(CommandHandler("forays_stopped", forays_stopped))
dp.add_handler(CommandHandler("send_message", send_message))

#On non command...
dp.add_handler(MessageHandler(Filters.text, echo))

#Start the bot
updater.start_polling()

#Run the bot until you press Ctrl+C
updater.idle()