import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def activities(driver, designators_data):
    wait = WebDriverWait(driver, 10)

    try:
        print("Localizando barra de busca...")

        # Input inicial quando a tela é carregada (sem nenhuma interação)
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Pesquisa em atividades")]')))

        if search_input:
            print("Barra de busca localizada!")
        else:
            print("Barra de busca não encontrada!")

        # designators_data = ['PAE-V0001QJB68-013', 'PAE-V0001QPR9M-013', 'PAE-V0001QJ00O-013']

        for designator in designators_data:
            print(designator)

            # Acionando o input que será carregado dinamicamente pela página (com interação)
            search_input.send_keys(Keys.ENTER)

            # Redefinindo o XPATH do input que fará a busca do designador
            search_input_clicked = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-bar-container"]/div[2]/div/div[1]/input')))

            # Inserindo o designador na barra de busca
            search_input_clicked.send_keys(designator)

            # Retornando o resultado da busca
            search_input_clicked.send_keys(Keys.ENTER)

            try:
                result_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "activity-title")))
            
                print("Resultado encontrado!")

                result_input.click()

                customer_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/a')))

                customer_button.click()
                
                # Campo nome cliente
                try:
                    customer_name_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "id_index_41")))
                    print(customer_name_field.text)
                except TimeoutException:
                    customer_name_field = "Não encontrado"
                    print("Campo nome cliente não encontrado!")

                # Campo email cliente
                try:
                    customer_email_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[6]/div[1]/div/a')))
                    print(customer_email_field.text)
                except TimeoutException:
                    customer_email_field = "Não encontrado"
                    print("Campo email não encontrado!")

                # Campo contato cliente
                try:
                    customer_contact_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[7]/div[1]/div/a')))
                    print(customer_contact_field.text)
                except TimeoutException:
                    customer_contact_field = "Não encontrado"
                    print("Campo contato não encontrado!")

                # Campo contato 2 cliente
                try:
                    customer_contact2_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[10]/div[1]/div/a')))
                    print(customer_contact2_field.text)
                except TimeoutException:
                    customer_contact2_field = "Não encontrado"
                    print("Campo contato 2 não encontrado!")

                # Campo contato alternativo cliente
                try:
                    customer_alternative_contact_field = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[12]/div[1]/div/a')))
                    print(customer_alternative_contact_field.text)
                except TimeoutException:
                    customer_alternative_contact_field = "Não encontrado"
                    print("Campo contato alternativo não encontrado!")

                driver.back()
                driver.back()
            except TimeoutException:
                print("Resultado não encontrado!")
                
                search_input_clicked.clear()
                search_input.send_keys(Keys.ENTER)

                pass

    except TimeoutException as exception:
            if len(exception.args) > 0:
                error_message = exception.args[0]
                logging.error(error_message)
            else:
                logging.error("Ocorreu uma exceção, mas nenhuma mensagem de erro foi retornada.")