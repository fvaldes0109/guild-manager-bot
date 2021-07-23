from modules import str_search
import mysql.connector
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

def addReport(id, report_msg):
    ptr = dbConnect()
    if searchPlayer(id, ptr) == True: #Only register report if the player is registered
        reportData = str_search.dataFromReport(report_msg)
        query = "INSERT INTO reports(player_id, exp, gold) VALUES (%s, %s, %s)"
        val = (id, reportData[0], reportData[1])
        ptr[1].execute(query, val)
        ptr[0].commit()
        dbClose(ptr)