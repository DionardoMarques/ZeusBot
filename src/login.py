import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def performLogin(driver, zeus_user, zeus_password):
    wait = WebDriverWait(driver, 10)
    attemps = 7
    delay = 5

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
                    else:
                        print("Manifest attribute não encontrado, prosseguindo...")
                except:
                    pass
            else:
                print("Botão de signin está desabilitado. Não é possível continuar.")

            # Verificando se a senha está incorreta
            try:
                print("Verificando se a senha está incorreta...")

                wrong_password_alert = wait.until(EC.presence_of_element_located((By.ID, "notification-message-block")))
                password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = wait.until(EC.presence_of_element_located((By.ID, "sign-in")))

                password_input.send_keys(zeus_password)
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        break
                    else:
                        print("Manifest attribute não encontrado, prosseguindo...")
                except:
                    pass
            except TimeoutException:
                pass

            # Verificando se o número de sessões foi excedido
            try:
                print("Verificando se o número de sessões foi excedido...")

                delsession_checkbox = wait.until(EC.presence_of_element_located((By.ID, "delsession")))
                password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = wait.until(EC.presence_of_element_located((By.ID, "sign-in")))
                
                password_input.send_keys(zeus_password)
                delsession_checkbox.click()
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        break
                    else:
                        print("Manifest attribute não encontrado, prosseguindo...")
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