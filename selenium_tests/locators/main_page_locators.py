from selenium.webdriver.common.by import By

class MainPageLocators:
    xpath_header_user_auth = (By.XPATH, '//*[@id="app-header-user"]/span')
    xpath_title_overview = (By.XPATH, '//*[@id="main-content"]/div/div[1]/h1')
    xpath_title_system_info = (By.XPATH, '//*[@id="main-content"]/div/div[3]/h2')
    xpath_model_server_inf = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/dl/dd[1]')
    xpath_server_manufacturer_inf = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[1]/div[1]/div/div/div[2]/div[2]/dl/dd')
    xpath_serial_number_inf = (By.XPATH, '//*[@id="main-content"]/div/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/dl/dd[2]')


