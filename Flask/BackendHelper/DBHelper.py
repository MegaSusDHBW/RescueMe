import pymysql

def connect():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="rescueme"
    )

    return mydb

def createDB():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
    )

    cursor = mydb.cursor()
    cursor.execute('CREATE DATABASE rescueme')

def insertInDB(mydb, client, key):
    sql = "INSERT INTO clientkey (client, key) VALUES (%s, %s)"
    val = (client, key)

    mydb.cursor().execute(sql, val)
    mydb.commit()