import mysql.connector

def connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="mydatabase"
    )

    return mydb

def insertInDB(mydb, client, key):
    sql = "INSERT INTO clientkey (client, key) VALUES (%s, %s)"
    val = (client, key)

    mydb.cursor().execute(sql, val)
    mydb.commit()