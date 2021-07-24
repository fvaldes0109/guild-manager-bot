from modules import str_search
import MySQLdb
import os

def dbConnect():
    mydb = mysql.connector.connect(
    host = os.environ['dbhost'],
    user = os.environ['dbuser'],
    password = os.environ['dbpassword'],
    database = os.environ['dbname']
    )
    mycursor = mydb.cursor()
    return [mydb, mycursor]

def dbClose(ptr):
    ptr[1].close()
    ptr[0].close()

def addPlayer(id, me_msg):
    ptr = dbConnect()
    playerData = str_search.dataFromMe(me_msg)
    query = ""
    val = ""
    if searchPlayer(id, ptr) == False:
        query = "INSERT INTO players VALUES (%s, %s, %s, %s)"
        val = (id, playerData[0], playerData[1], playerData[2])
    else:
        query = "UPDATE players SET guild = %s, playername = %s, class = %s WHERE player_id = %s"
        val = (playerData[0], playerData[1], playerData[2], id)
    ptr[1].execute(query, val)
    ptr[0].commit()
    dbClose(ptr)
        
def searchPlayer(id, ptr):
    query = "SELECT player_id FROM players WHERE player_id = '" + str(id) + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    if len(result) == 0:
        return False
    else:
        return True

def addReport(id, report_msg, date):
    ptr = dbConnect()
    if searchPlayer(id, ptr) == True: #Only register report if the player is registered
        reportData = str_search.dataFromReport(report_msg)
        if samePlayer(reportData[2], reportData[3], ptr) and reportStored(id, date, ptr) == False:
            query = "INSERT INTO reports(player_id, exp, gold, date) VALUES (%s, %s, %s, %s)"
            val = (id, reportData[0], reportData[1], date)
            ptr[1].execute(query, val)
            ptr[0].commit()
            dbClose(ptr)

def samePlayer(guild, name, ptr):
    query = "SELECT * FROM players WHERE guild = '" + guild + "' AND playername = '" + name + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    if len(result) == 0:
        return False
    else:
        return True

def reportStored(id, date, ptr):
    query = "SELECT * FROM reports WHERE player_id = '" + str(id) + "' AND date = '" + date + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    if len(result) == 0:
        return False
    else:
        return True

def weeklyWipeReports():
    ptr = dbConnect()
    query = "DELETE FROM reports"
    ptr[1].execute(query)
    ptr[0].commit()
    dbClose(ptr)

def getAttendance(id):
    ptr = dbConnect()
    query = "SELECT guild FROM players WHERE player_id ='" + str(id) + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    guild = result[0][0]
    query = "SELECT playername, COUNT(report_id) FROM players, reports "
    query = query + "WHERE players.player_id = reports.player_id AND players.guild = '" + guild
    query = query + "' GROUP BY playername"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    dbClose(ptr)
    return [guild, result]

def getExp(id):
    ptr = dbConnect()
    query = "SELECT guild FROM players WHERE player_id ='" + str(id) + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    guild = result[0][0]
    query = "SELECT playername, SUM(exp) FROM players, reports "
    query = query + "WHERE players.player_id = reports.player_id AND players.guild = '" + guild
    query = query + "' GROUP BY playername"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    dbClose(ptr)
    return [guild, result]

def getGold(id):
    ptr = dbConnect()
    query = "SELECT guild FROM players WHERE player_id ='" + str(id) + "'"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    guild = result[0][0]
    query = "SELECT playername, SUM(gold) FROM players, reports "
    query = query + "WHERE players.player_id = reports.player_id AND players.guild = '" + guild
    query = query + "' GROUP BY playername"
    ptr[1].execute(query)
    result = ptr[1].fetchall()
    dbClose(ptr)
    return [guild, result]
