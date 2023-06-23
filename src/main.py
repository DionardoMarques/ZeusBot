import os
import time
import logging
import database

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login import performLogin

load_dotenv()

# Credenciais ZEUS
conn_db = database.MySQLConnection()
zeus_credentials = database.getUser(conn_db)
zeus_user = zeus_credentials[0][0]
zeus_password = zeus_credentials[0][1]

# WebDriver Chrome (114.0.5735.90)
webdriver_path = os.getenv("DRIVER_PATH") 
url = os.getenv("ZEUS_URL")

# Parâmetros
options = Options()
options.page_load_strategy = 'eager' # Elementos do DOM prontos, mas outros recursos como imagens talvez continuem carregando
options.add_argument("--ignore-certificate-errors")
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

status_login = performLogin(driver, zeus_user, zeus_password)
print(status_login)

input("Pressione enter para fechar a janela do navegador...")

# Fechando a instância do Webdriver
driver.quit()