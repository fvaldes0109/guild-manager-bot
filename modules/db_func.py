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
    query = "INSERT INTO players VALUES (%s, %s, %s, %s)"
    val = (id, playerData[0], playerData[1], playerData[2])
    ptr[1].execute(query, val)
    ptr[0].commit()
    dbClose(ptr)
