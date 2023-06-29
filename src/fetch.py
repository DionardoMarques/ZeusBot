import time
import logging

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def activities(driver, designators_data):
    wait = WebDriverWait(driver, 10)
    zeus_data = []

    for designator_tuple in designators_data:
        try:
            # Input inicial quando a tela é carregada (sem nenhuma interação)
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Pesquisa em atividades")]')))

            designator = designator_tuple[0] # Formatando o desginador Ex: ('PAE-V0001QJIRO-013',) Será: PAE-V0001QJIRO-013

            now = datetime.now()
            start_date = now.strftime("%m/%d/%Y %H:%M:%S")

            print(designator)

            # Acionando o input que será carregado dinamicamente pela página (com interação)
            search_input.send_keys(Keys.ENTER)

            # Redefinindo o XPATH do input que fará a busca do designador
            search_input_clicked = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-bar-container"]/div[2]/div/div[1]/input')))

            # Inserindo o designador na barra de busca
            search_input_clicked.send_keys(designator)

            # Retornando o resultado da busca
            search_input_clicked.send_keys(Keys.ENTER)

            result_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "activity-title")))
        
            print("Resultado encontrado!")

            result_input.click()

            customer_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/a')))
            customer_button.click()
            
            # Campo nome cliente
            try:
                customer_name_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "id_index_41")))
                customer_name_field = customer_name_field.text
            except TimeoutException:
                customer_name_field = "Nao encontrado"

            # Campo email cliente
            try:
                customer_email_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[6]/div[1]/div/a')))
                customer_email_field = customer_email_field.text
            except TimeoutException:
                customer_email_field = "Nao encontrado"

            # Campo contato cliente
            try:
                customer_contact_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[7]/div[1]/div/a')))
                customer_contact_field = customer_contact_field.text
            except TimeoutException:
                customer_contact_field = "Nao encontrado"

            # Campo contato 2 cliente
            try:
                customer_contact2_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[10]/div[1]/div/a')))
                customer_contact2_field = customer_contact2_field.text
            except TimeoutException:
                customer_contact2_field = "Nao encontrado"

            # Campo contato alternativo cliente
            try:
                customer_alternative_contact_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[12]/div[1]/div/a')))
                customer_alternative_contact_field = customer_alternative_contact_field.text
            except TimeoutException:
                customer_alternative_contact_field = "Nao encontrado"

            now = datetime.now()
            end_date = now.strftime("%m/%d/%Y %H:%M:%S")

            # Armazenando os dados do cliente junto ao seu designador correspondente
            zeus_data.append([designator, customer_name_field, customer_email_field, customer_contact_field, customer_contact2_field, customer_alternative_contact_field, 'sem erro', start_date, end_date])

            driver.back()
            driver.back()
            
        except Exception as exception:
            logging.basicConfig(filename='logs/db_exceptions.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')
            
            now = datetime.now()
            end_date = now.strftime("%m/%d/%Y %H:%M:%S")

            if isinstance(exception, TimeoutException):
            # Designadores não encontrados no ZEUS
                print("Resultado não encontrado!")

                customer_name_field = "Nao encontrado"
                customer_email_field = "Nao encontrado"
                customer_contact_field = "Nao encontrado"
                customer_contact2_field = "Nao encontrado"
                customer_alternative_contact_field = "Nao encontrado"

                zeus_data.append([designator, customer_name_field, customer_email_field, customer_contact_field, customer_contact2_field, customer_alternative_contact_field, 'sem erro', start_date, end_date])

                search_input_clicked.clear()
                search_input.send_keys(Keys.ENTER)

                pass
            else:
                logging.error(exception)
                
                zeus_data.append([designator, 'E', 'E', 'E', 'E', 'E', exception, start_date, end_date])

                print("Recarregando a página...")
                driver.refresh()

                pass

    return zeus_data