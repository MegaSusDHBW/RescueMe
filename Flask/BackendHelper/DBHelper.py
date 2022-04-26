import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('dbUser')
key = os.getenv('dbKey')
dbpath = f'mysql+pymysql://{user}:{key}@178.63.84.105:3306/mobs'

def connect():
    mydb = pymysql.connect(
        host="178.63.84.105",
        user=user,
        password=key,
        database="mobs"
    )
    return mydb

def insertInDB(mydb, client, key):
    sql = "INSERT INTO clientkey (client, key) VALUES (%s, %s)"
    val = (client, key)

    mydb.cursor().execute(sql, val)
    mydb.commit()