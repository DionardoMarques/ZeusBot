import os
import time
import logging
import mysql.connector
import firebirdsql

import logger

from datetime import date
from datetime import datetime
from datetime import timedelta

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
        password = os.getenv("PASSWORD_FIREBIRD"),
        charset='UTF8'
    )

    return conn_firebird

def fetchData(conn_firebird):
    current_date = date.today()

    promise_date = current_date + timedelta(days=1)
    promise_date = promise_date.strftime("%m/%d/%Y")

    expiration_date = current_date + timedelta(days=2)
    expiration_date = expiration_date.strftime("%m/%d/%Y")

    # Codificando o acento para o Firebird
    available_filter = 'DISPONÍVEL'.encode('iso-8859-1')

    sql = conn_firebird.cursor()
    # BA e TT
    # sql.execute("SELECT DISTINCT DESIGNADOR FROM (SELECT DISTINCT CADBACKLOG.INSTANCIA AS DESIGNADOR FROM CADBACKLOG INNER JOIN CADCONTATO ON (CADBACKLOG.INSTANCIA = CADCONTATO.DESIGNADOR AND CADCONTATO.ATUALIZACAO IS NULL) WHERE CADBACKLOG.DATA_PROMESSA = ? AND CADBACKLOG.STATUS_BA = 'AGENDADA' AND CADBACKLOG.SERVICO = ? AND CADBACKLOG.INSTANCIA <> '0' UNION ALL SELECT DISTINCT CADBACKTT.ISNTANCIA AS DESIGNADOR FROM CADBACKTT INNER JOIN CADCONTATO ON (CADBACKTT.ISNTANCIA = CADCONTATO.DESIGNADOR AND CADCONTATO.ATUALIZACAO IS NULL) WHERE CADBACKTT.VENCIMENTO >= ? AND CADBACKTT.VENCIMENTO < ? AND CADBACKTT.STATUS = 'AGENDADA' AND CADBACKTT.EMPRESA = 'TLSV') ORDER BY DESIGNADOR", (promise_date, available_filter, promise_date, expiration_date))
    
    # Apenas BA e CLUSTER PAE
    sql.execute("SELECT FIRST 1 DISTINCT DESIGNADOR FROM (SELECT DISTINCT CADBACKLOG.INSTANCIA AS DESIGNADOR FROM CADBACKLOG INNER JOIN CADCONTATO ON (CADBACKLOG.INSTANCIA = CADCONTATO.DESIGNADOR AND CADCONTATO.ATUALIZACAO IS NULL) WHERE CADBACKLOG.DATA_PROMESSA = ? AND CADBACKLOG.STATUS_BA = 'AGENDADA' AND CADBACKLOG.SERVICO = ? AND CADBACKLOG.CLUSTER = 'CLUSTER PAE' AND CADBACKLOG.INSTANCIA <> '0') ORDER BY DESIGNADOR", (promise_date, available_filter))
    data = sql.fetchall()

    return data

def updateData(conn_firebird, zeus_data):
    now = datetime.now()
    update_date = now.strftime("%m/%d/%Y %H:%M:%S")

    for data in zeus_data:
        print(data)
        
        designator = data[0]
        customer_name = data[1]
        customer_email = data[2]
        customer_contact = data[3]
        customer_contact2 = data[4]
        customer_contact3 = data[5]
        log = data[6]
        start_date = data[7]
        end_date = data[8]

        #Update na tabela CAD_CONTATO Firebird
        try:
            sql = conn_firebird.cursor()
            
            if customer_name == 'E' or customer_email == 'E' or customer_contact == 'E' or customer_contact2 == 'E' or customer_contact3 == 'E':
                sql.execute("UPDATE CADCONTATO SET NOME = ?, EMAIL = ?, CONTATO = ?, CONTATO2 = ?, CONTATO3 = ?, INICIO = ?, TERMINO = ?, LOG = ? WHERE DESIGNADOR = ?", (customer_name, customer_email, customer_contact, customer_contact2, customer_contact3, start_date, end_date, log, designator))
            else:
                sql.execute("UPDATE CADCONTATO SET NOME = ?, EMAIL = ?, CONTATO = ?, CONTATO2 = ?, CONTATO3 = ?, INICIO = ?, TERMINO = ?, LOG = ?, ATUALIZACAO = ? WHERE DESIGNADOR = ?", (customer_name, customer_email, customer_contact, customer_contact2, customer_contact3, start_date, end_date, log, update_date, designator))
            
            conn_firebird.commit()

            print("Atualização de dados realizada com sucesso!")
        except Exception as exception:
            conn_firebird.rollback()

            db_logger = logger.setupLogger('db_logs', 'logs/db_exceptions.log')
            db_logger.exception(exception)

            print(f"Update falhou: {str(exception)}")