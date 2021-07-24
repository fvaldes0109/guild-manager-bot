import emoji

start = """Bienvenido!
Reenvia un /me para registrarte"""

help = """Comandos:
/reports - Muestra la asistencia semanal a la batalla de los guildmates
/reports_exp - Muestra la ganancia de exp semanal por batalla
/reports_gold - Muestra la ganancia de oro semanal por batalla"""

def comp(e):
    return e[1]

def attendance(guild, att, count):
    msg = emoji.emojize(":crossed_swords:<b><u>Asistencia semanal de [" + guild + "]</u></b>\n\n")
    att = list(att)
    att.sort(reverse = True, key = comp)
    i = 1
    for pair in att:
        percent = int(pair[1] * 100 / count)
        msg = msg + emoji.emojize(str(i) + ". " + pair[0] + " - :crossed_swords:" + str(pair[1]) + " / ")
        msg = msg + str(count) + " (" + str(percent) + "%)\n"
        i = i + 1
    return msg

def expReports(guild, l):
    msg = emoji.emojize(":fire:<b><u>Experiencia de la semana [" + guild + "]</u></b>\n\n")
    l = list(l)
    l.sort(reverse = True, key = comp)
    i = 1
    for pair in l:
        msg = msg + emoji.emojize(str(i) + ". " + pair[0] + " - :fire:" + str(pair[1]) + "\n")
        i = i + 1
    return msg

def goldReports(guild, l):
    msg = emoji.emojize(":money_bag:<b><u>Oro de la semana [" + guild + "]</u></b>\n\n")
    l = list(l)
    l.sort(reverse = True, key = comp)
    i = 1
    for pair in l:
        msg = msg + emoji.emojize(str(i) + ". " + pair[0] + " - :money_bag:" + str(pair[1]) + "\n")
        i = i + 1
    return msg
        
