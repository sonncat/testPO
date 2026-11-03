from selenium.webdriver.common.by import By

class LoginPageLocators:
    xpath_login =(By.XPATH, '//*[@id="username"]')
    xpath_password = (By.XPATH, '//*[@id="password"]')
    xpath_login_button = (By.XPATH, '//*[@id="app"]/main/div/div[1]/div/form/button')
    xpath_login_alert_error = (By.XPATH, '//*[@id="app"]/main/div/div[1]/div/form/div[1]')
    xpath_login_error_text = (By.XPATH, '//*[@id="login-error-alert"]')