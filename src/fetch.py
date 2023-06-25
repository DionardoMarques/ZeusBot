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

            result_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "activity-title")))

            if result_input:
                print("Resultado encontrado!")
            else:
                print("Resultado não encontrado!")

            result_input.click()

            customer_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[1]/div[2]/div/div[2]/div[1]/div/a')))

            if customer_button:
                print("Botão encontrado!")
            else:
                print("Botão não encontrado!")

            customer_button.click()

            customer_name_field = wait.until(EC.presence_of_element_located((By.ID, "id_index_41")))
            customer_email_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[6]/div[1]/div/a')))
            customer_contact_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[7]/div[1]/div/a')))
            customer_contact2_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="context-layout"]/div/div/div[2]/div/div/div[2]/div[10]/div[1]/div/a')))

            print(customer_name_field.text)
            print(customer_email_field.text)
            print(customer_contact_field.text)
            print(customer_contact2_field.text)

            driver.back()
            driver.back()

    except TimeoutException as exception:
            if len(exception.args) > 0:
                error_message = exception.args[0]
                logging.error(error_message)
            else:
                logging.error("Ocorreu uma exceção, mas nenhuma mensagem de erro foi retornada.")