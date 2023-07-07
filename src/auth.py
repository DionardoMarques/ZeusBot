import time
import logging

import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login(driver, zeus_user, zeus_password):
    wait = WebDriverWait(driver, 5)
    attemps = 7
    delay = 10

    status_login = False

    auth_logger = logger.setupLogger('auth_logs', r'C:\projects\ZeusBot\logs\auth.log')

    # Realizando login
    for attempt in range(1, attemps + 1):
        try:
            print(f"Tentativa de login: {attempt}")

            print("Realizando login...")

            username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))

            username_input.clear()
            password_input.clear()

            username_input.send_keys(zeus_user)
            password_input.send_keys(zeus_password)

            signin_button = wait.until(EC.presence_of_element_located((By.ID, "sign-in")))
            
            if signin_button.get_attribute("disabled") is None:
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True
                        
                        auth_logger.info(f"Login realizado com sucesso! Quantidade de tentativas: {attempt}")

                        break
                except:
                    pass

            # Verificando se a senha está incorreta
            try:
                print("Verificando se a senha está incorreta...")

                wrong_password_alert = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "notification-message-block")))
                username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
                password_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "sign-in")))

                username_input.clear()
                password_input.clear()

                username_input.send_keys(zeus_user)
                password_input.send_keys(zeus_password)

                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True

                        auth_logger.info(f"Login realizado com sucesso! Quantidade de tentativas: {attempt}")

                        break
                except:
                    pass
            except:
                pass

            # Verificando se o número de sessões foi excedido
            try:
                print("Verificando se o número de sessões foi excedido...")

                delsession_checkbox = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "delsession")))
                username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
                password_input = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "password")))
                signin_button = WebDriverWait(driver, 1).until  (EC.presence_of_element_located((By.ID, "sign-in")))

                username_input.clear()
                password_input.clear()
                
                username_input.send_keys(zeus_user)
                password_input.send_keys(zeus_password)

                delsession_checkbox.click()
                signin_button.click()

                try:
                    manifest_attribute = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "html[manifest]")))

                    if manifest_attribute:
                        status_login = True

                        auth_logger.info(f"Login realizado com sucesso! Quantidade de tentativas: {attempt}")

                        break
                except:
                    pass
            except:
                pass
                
        except Exception as exception:
            print(f"Erro durante login: {str(exception)}")

            auth_logger.exception(exception)

            pass

        # Delay para tentar novamente o login e não levar timeout do ZEUS
        time.sleep(delay)

    return status_login

def logout(driver):
    logout_logger = logger.setupLogger('logout_logs', r'C:\projects\ZeusBot\logs\logout_exceptions.log')
    wait = WebDriverWait(driver, 5)
    
    try:
        print("Fazendo logout...")
    
        user_menu_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-menu-region")))
        user_menu_button.click()

        logout_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item-caption--logout")))
        logout_button.click()

        print("Logout realizado!")
    except Exception as exception:
        logout_logger.exception(f"Erro ao tentar deslogar o usuário atual: {str(exception)}")
