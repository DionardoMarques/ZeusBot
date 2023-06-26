import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login(driver, zeus_user, zeus_password):
    wait = WebDriverWait(driver, 5)
    attemps = 7
    delay = 10

    status_login = False

    for attempt in range(1, attemps + 1):
        print(f"Tentativa de login: {attempt}")

        try:
            print("Realizando login...")
            # Realizando login
            username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))

            username_input.send_keys(zeus_user)
            password_input.send_keys(zeus_password)

            signin_button = wait.until(EC.presence_of_element_located((By.ID, "sign-in")))
            
            if signin_button.get_attribute("disabled") is None:
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        break
                except:
                    pass

            # Verificando se a senha está incorreta
            try:
                print("Verificando se a senha está incorreta...")

                wrong_password_alert = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "notification-message-block")))
                password_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "sign-in")))

                password_input.send_keys(zeus_password)
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        break
                except:
                    pass
            except TimeoutException:
                pass

            # Verificando se o número de sessões foi excedido
            try:
                print("Verificando se o número de sessões foi excedido...")

                delsession_checkbox = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "delsession")))
                password_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "sign-in")))
                
                password_input.send_keys(zeus_password)
                delsession_checkbox.click()
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        break
                except:
                    pass
            except TimeoutException:
                pass

        except TimeoutException as exception:
            if len(exception.args) > 0:
                error_message = exception.args[0]
                logging.error(error_message)
            else:
                logging.error("Ocorreu uma exceção, mas nenhuma mensagem de erro foi retornada.")
        
        # Delay para tentar novamente o login e não levar timeout do ZEUS
        time.sleep(delay)

    return status_login

def logout(driver):
    wait = WebDriverWait(driver, 5)
    
    print("Fazendo logout...")

    user_menu_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-menu-region")))
    
    # Clicando no menu superior direito
    user_menu_button.click()

    logout_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item-caption--logout")))
    logout_button.click()