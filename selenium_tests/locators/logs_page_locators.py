from selenium.webdriver.common.by import By

class LogsPageLocators:
    xpath_logs_title = (By.XPATH, '//*[@id="main-content"]/div/div[1]')
    xpath_table_none_logs = (By.XPATH, '//*[@id="table-event-logs"]/tbody/tr/td/div/div')
    