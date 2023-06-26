import os
from datetime import date
import mysql.connector
import firebirdsql

from dotenv import load_dotenv

def MySQLConnection():
    load_dotenv()

    conn_mysql = mysql.connector.connect(
        host = os.getenv("HOST_MYSQL"),
        database = os.getenv("DATABASE_MYSQL"),
        user = os.getenv("USER_MYSQL"),
        password = os.getenv("PASSWORD_MYSQL")
    )
    
    return conn_mysql

def getUser(conn_mysql):
    sql = conn_mysql.cursor()
    sql.execute("SELECT usuario, senha FROM gb_login WHERE ID = 6")
    data = sql.fetchall()

    return data

def FirebirdConnection():
    load_dotenv()

    conn_firebird = firebirdsql.connect(
        host = os.getenv("HOST_FIREBIRD"),
        database = os.getenv("DATABASE_FIREBIRD"),
        user = os.getenv("USER_FIREBIRD"),
        password = os.getenv("PASSWORD_FIREBIRD")
    )

    return conn_firebird

def fetchData(conn_firebird):
    current_date = date.today()

    sql = conn_firebird.cursor()
    sql.execute("SELECT CADRESDIA.INSTANCIA FROM CADRESDIA WHERE CADRESDIA.DATA_AGENDAMENTO >= ? AND CADRESDIA.STATUS = 'E' AND CADRESDIA.CIDADE = 'PORTO ALEGRE'", (current_date,))
    data = sql.fetchall()

    conn_firebird.close()

    return data

def insertData(zeus_data):
    current_date = date.today()

    for data in zeus_data:
        print(data)