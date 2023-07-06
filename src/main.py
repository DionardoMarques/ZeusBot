import os
import time
import logging
import socket
import threading

import db
import auth
import fetch
import notify
import logger

from dotenv import load_dotenv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()

HOST = ''
PORT = 1234

stop_flag = False
is_running = False
lock = threading.Lock()

def startBot():
    global is_running

    lock.acquire()

    try:
        if is_running:
            return

        # Set the flag to indicate that the function is running
        is_running = True

        now = datetime.now()
        start_date = now.strftime("%d/%m/%Y %H:%M:%S")
        start_time = now.strftime("%H:%M:%S")

        # Email bot iniciado
        notify.botStarted(start_date)

        # Credenciais ZEUS
        conn_mysql = db.MySQLConnection()
        zeus_credentials = db.getUser(conn_mysql)
        zeus_user = zeus_credentials[0][0]
        zeus_password = zeus_credentials[0][1]

        # WebDriver Chrome (114.0.5735.90)
        webdriver_path = os.getenv("DRIVER_PATH") 
        url = os.getenv("ZEUS_URL")

        # Parâmetros
        options = Options()
        options.page_load_strategy = 'eager' # Elementos do DOM prontos, mas outros recursos como imagens talvez continuem carregando
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-notifications")
        options.add_argument("--headless=new") # Não abre a interface do navegador
        # options.add_argument("--start-maximized") # Abre em tela cheia o navegador

        # Inicializando a instância do Webdriver
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        # Realizando login
        status_login = auth.login(driver, zeus_user, zeus_password)

        if status_login == True:
            # Dados designador
            conn_firebird = db.FirebirdConnection()
            designators_data = db.fetchData(conn_firebird)
            
            # Buscando os dados dos clientes no ZEUS
            zeus_data = fetch.activities(driver, designators_data)
            
            # Atualizando os dados da tabela CAD_CONTATO com os dados coletados do ZEUS
            db.updateData(conn_firebird, zeus_data)

            conn_firebird.close()

            # Deslogando
            auth.logout(driver)
            time.sleep(1)
        else:
            notify.wrongPassword()

        now = datetime.now()
        end_date = now.strftime("%d/%m/%Y %H:%M:%S")
        end_time = now.strftime("%H:%M:%S")

        start_datetime = datetime.strptime(start_time, "%H:%M:%S")
        end_datetime = datetime.strptime(end_time, "%H:%M:%S")

        duration = end_datetime - start_datetime

        print("Total atividades:", len(zeus_data))
        print("Tempo total de duração:", duration)
        print("Data e hora início:", start_date)
        print("Data e hora fim:", end_date)

        main_logger = logger.setupLogger('main_logs', r'C:\projects\ZeusBot\logs\main.log')
        main_logger.info(f"\nTotal atividades: {str(len(zeus_data))}\nTempo total: {str(duration)}\nData e hora inicio: {str(start_date)}\nData e hora fim: {str(end_date)}")

        # Email bot finalizado
        notify.botFinished(end_date, start_date, duration, zeus_data)

        # Fechando a instância do Webdriver
        driver.quit()
    finally:
        is_running = False
        lock.release()
    
def handleConnection(conn):
    address = conn.getpeername()
    print("Conexao estabelecida com:", address)

    command = conn.recv(1024).decode()
    print(command)

    if command == 'IniciarRobo':
        startBot()

    conn.close()

    print("Conexao encerrada com:", address)
    print("Aguardando conexoes...")

def waitConnection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Aguardando conexoes...")

    while True:
        conn, address = server.accept()

        thread = threading.Thread(target=handleConnection, args=(conn,))
        thread.start()

if __name__ == "__main__":
    try:
        main_thread = threading.Thread(target=waitConnection)
        main_thread.daemon = True 
        main_thread.start()

        while True:
            if stop_flag:
                break

    except KeyboardInterrupt:
        print("Comando de interrupção recebido, parando o script...")
        stop_flag = True

    notify.shutDownBot()

    print("Script finalizado.")