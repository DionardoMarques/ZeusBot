import os
import mysql.connector
from dotenv import load_dotenv

def MySQLConnection ():
    load_dotenv()

    conn_db = mysql.connector.connect(
        host = os.getenv("HOST"),
        database = os.getenv("DATABASE"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD")
    )
    
    return conn_db

def getUser (conn_db):
    sql = conn_db.cursor()
    sql.execute("SELECT usuario, senha FROM gb_login WHERE ID = 6")
    data = sql.fetchall()

    return data