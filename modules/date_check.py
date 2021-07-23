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