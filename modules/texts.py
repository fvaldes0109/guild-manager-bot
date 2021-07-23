import emoji

start = """Bienvenido!
Reenvia un /me para registrarte"""

help = """Este es el texto de ayuda"""

def comp(e):
    return e[1]

def attendance(guild, att, count):
    msg = "<b><u>Asistencia a la batalla de [" + guild + "]</u></b>\n\n"
    att.sort(reverse = True, key = comp)
    i = 1
    for pair in att:
        percent = int(pair[1] * 100 / count)
        msg = msg + emoji.emojize(str(i) + ". " + pair[0] + " - :crossed_swords:" + str(pair[1]) + " / ")
        msg = msg + str(count) + " (" + str(percent) + "%)\n"
        i = i + 1
    return msg
        