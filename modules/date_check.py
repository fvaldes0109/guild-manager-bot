from datetime import datetime, timedelta
import pytz

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