import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def activities(driver, designators_data):
    wait = WebDriverWait(driver, 10)

    try:
        print("Localizando barra de busca...")

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Pesquisa em atividades")]')))
        # search_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-bar-input')))
        # search_input = wait.until(EC.presence_of_element_located((By.ID, "elId294")))

        if search_input:
            print("Barra de busca localizada!")
        else:
            print("Barra de busca não encontrada!")

        for designator in designators_data:
            print(designator)

            search_input.send_keys(Keys.RETURN)

            time.sleep(5)

            script = """
                var designator = arguments[0];

                var searchInput = document.querySelector('input[data-bind^="textInput"]');
                searchInput.value = designator;

                // Trigger the necessary events to update the input field
                var event = new Event('input', { bubbles: true });
                searchInput.dispatchEvent(event);
                event = new Event('change', { bubbles: true });
                searchInput.dispatchEvent(event);

                // Trigger the Enter key event on the input field
                var enterEvent = new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', which: 13, keyCode: 13, bubbles: true });
                searchInput.dispatchEvent(enterEvent);
            """

            driver.execute_script(script, designator)

            # time.sleep(2)
            # # Move the mouse to the search_input element to activate it
            # ActionChains(driver).move_to_element(search_input).perform()
            # print("Action concluida")
            # time.sleep(2)

            # Insert the designator into the active search_input element
            # search_input.send_keys(designator)
            # print("Inserido o designador")
            # time.sleep(2)

            # # Simulate pressing Enter to trigger the search
            # search_input.send_keys(Keys.RETURN)
            # print("Apertado o enter")
            # time.sleep(2)

            # driver.execute_script("arguments[0].value = arguments[1];", search_input, designator)
            # print("Tentativa de inserção!")
            # time.sleep(5)

            # driver.execute_script("arguments[0].click();", search_input)
            # driver.execute_script("arguments[0].click();", search_input)
            
            # search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Pesquisa em atividades")]')))
            # time.sleep(5)
            # search_input.send_keys(designator)
            # search_input.click()
            # driver.execute_script("arguments[0].click();", search_input)

            # search_input.send_keys(Keys.RETURN)

            # search_input.send_keys(designator)

            # search_input.send_keys("PAE")
            # time.sleep(5)
            # search_input.clear()
            # search_input.click()
            # search_input.clear()

            # result_input = wait.until(EC.presence_of_element_located((By.ID, "oj-collapsible-10-content")))

            # if result_input:
            #     print("Resultado encontrado!")
            # else:
            #     print("Resultado não encontrado!")

            # result_input.click()

    except TimeoutException as exception:
            if len(exception.args) > 0:
                error_message = exception.args[0]
                logging.error(error_message)
            else:
                logging.error("Ocorreu uma exceção, mas nenhuma mensagem de erro foi retornada.")