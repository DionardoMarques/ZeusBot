import os
import time
import logging

import db
import auth
import fetch

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv()

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
# options.add_argument("--start-maximized") # Abre em tela cheia o navegador
# options.add_argument("--headless=new") # Não abre a interface do navegador

# Inicializando a instância do Webdriver
driver = webdriver.Chrome(options=options)

# Simular internet lenta
# driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
#     'offline': False,
#     'downloadThroughput': 500 * 1024,
#     'uploadThroughput': 500 * 1024,
#     'latency': 4000
# })

driver.get(url)

# Realizando login
status_login = auth.login(driver, zeus_user, zeus_password)

if status_login == True:
    # Dados designador
    conn_firebird = db.FirebirdConnection()
    designators_data = db.fetchData(conn_firebird)
    
    # Buscando os dados dos clientes no ZEUS
    fetch.activities(driver, designators_data)

    # Deslogando
    auth.logout(driver)
    
input("Pressione enter para fechar a janela do navegador...")

# Fechando a instância do Webdriver
driver.quit()