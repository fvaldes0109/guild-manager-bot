from modules import str_search
import mysql.connector
import os

mycursor = None
mydb = None

def dbConnect():
    global mycursor
    global mydb
    mydb = mysql.connector.connect(
    host = os.environ['dbhost'],
    user = os.environ['dbuser'],
    password = os.environ['dbpassword'],
    database = os.environ['dbname']
    )
    mycursor = mydb.cursor()

def addPlayer(id, me_msg):
    playerData = str_search.dataFromMe(me_msg)
    query = "INSERT INTO players VALUES (%s, %s, %s, %s)"
    val = (id, playerData[0], playerData[1], playerData[2])
    mycursor.execute(query, val)
    mydb.commit()