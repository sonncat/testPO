from selenium.webdriver.common.by import By

class PowerControlLocators:
    xpath_power_control_title = (By.XPATH, '//*[@id="main-content"]/div/div[1]/h1')
    xpath_power_status = (By.XPATH, '    //*[@id="main-content"]/div/div[2]/div/div/div[1]/div/dl/dd')
    xpath_power_on_button = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[2]/div/button')
    xpath_alert_after_click_power = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div')
    xpath_button_shut_down = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[2]/div/form[2]/button')
    xpath_modal_server_shut_down = (By.XPATH, '//*[@id="global-confirm-modal-label"]')
    xpath_modal_shut_down_button = (By.XPATH, '//*[@id="global-confirm-modal"]/div/div/div[3]/button[2]')