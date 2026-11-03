from selenium.webdriver.common.by import By

class InventoryPageLocators:
    xpath_table_processor =(By.XPATH, '//*[@id="BootstrapVueNext__ID__v-83__"]/tbody/tr/td')
    xpath_title_table_processor = (By.XPATH, '//*[@id="main-content"]/div/div[10]/h2')
    xpath_count_item_processor = (By.XPATH, '//*[@id="main-content"]/div/div[10]/div[1]/div[2]/div/p')
    xpath_inventory_title = (By.XPATH, '//*[@id="main-content"]/div/div[1]/h1')