from datetime import datetime, timedelta
import pytz
from threading import Timer
from modules import db_func

def isRecent(date):
    current_date = datetime.today().astimezone(pytz.timezone('America/Havana'))
    forward_date = date.astimezone(pytz.timezone('America/Havana'))
    diff = (current_date - forward_date).total_seconds()
    if diff <= 120:
        return True
    else:
        return False

def getBattleDate(date):
    forward_date = date.astimezone(pytz.timezone('America/Havana'))
    hour = forward_date.hour
    forward_date = forward_date.replace(minute = 0, second = 0)
    if hour < 3:
        forward_date = forward_date.replace(hour = 19)
        forward_date = forward_date - timedelta(days = 1)
    elif hour < 11:
        forward_date = forward_date.replace(hour = 3)
    elif hour < 19:
        forward_date = forward_date.replace(hour = 11)
    else:
        forward_date = forward_date.replace(hour = 19)
    reportDate = forward_date.strftime("%Y-%m-%d %H:%M:%S")
    return reportDate

def getNextWipe():
    current = datetime.today().astimezone(pytz.timezone('America/Havana'))
    weekday = current.weekday()
    diff = 6 - weekday
    if diff == 0 and current.hour >= 20:
        diff = 7
    nextPoint = (current.replace(hour = 20, minute = 0, second = 0, microsecond = 0) + timedelta(days = diff)) - current
    print("Currently:", current)
    print("Next:", nextPoint)
    return nextPoint

def wipeReports(callback):
    callback()
    db_func.weeklyWipeReports()
    nextWipe = getNextWipe()
    wipe_timer = Timer(nextWipe.total_seconds(), wipeReports, [callback])
    wipe_timer.start()

def startTimers(callback):
    nextWipe = getNextWipe()
    wipe_timer = Timer(nextWipe.total_seconds(), wipeReports, [callback])
    wipe_timer.start()

def getBattleCount():
    current = datetime.today().astimezone(pytz.timezone('America/Havana'))
    weekday = current.weekday()
    hour = current.hour
    ind = 0
    if hour < 3:
        ind = 0
    elif hour < 11:
        ind = 1
    elif hour < 19:
        ind = 2
    else:
        ind = 3
    if weekday == 6 and hour > 20:
        return 0
    else:
        count = weekday * 3 + ind
        return count
