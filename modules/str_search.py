def dataFromMe(me_msg):
    pos = me_msg.find("Level: ")
    chop = me_msg[:pos - 2]
    l = chop.split('\n')
    playerData = l[-1]
    guild = getGuild(playerData)
    clase = getClass(playerData)
    name = playerData[guild[0] : clase[0]]
    return [guild[1], name, clase[1]]

def getGuild(msg):
    pos = msg.find('[')
    if pos != -1:
        pos2 = msg.find(']')
        return [pos2 + 1, msg[pos + 1: pos2]]
    else:
        return [1, ""]

def getClass(msg):
    fpos = msg.find("of ") - 1
    clase = ""
    pos = msg.find("Knight of")
    if pos != -1:
        return [pos - 1, "Knight"]
    pos = msg.find("Sentinel of")
    if pos != -1:
        return [pos - 1, "Sentinel"]
    pos = msg.find("Ranger of")
    if pos != -1:
        return [pos - 1, "Ranger"]
    pos = msg.find("Collector of")
    if pos != -1:
        return [pos - 1, "Collector"]
    pos = msg.find("Alchemist of")
    if pos != -1:
        return [pos - 1, "Alchemist"]
    pos = msg.find("Blacksmith of")
    if pos != -1:
        return [pos - 1, "Blacksmith"]
    pos = msg.find("Master of")
    if pos != -1:
        return [pos - 1, "Master"]
    return [fpos, ""]
    pos = msg.find("Esquire of")
    if pos != -1:
        return [pos - 1, "Esquire"]
    return [fpos, ""]