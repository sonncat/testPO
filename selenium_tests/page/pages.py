from page.base_page import BasePage
from page.login_page import LoginPage
from page.main_page import MainPage
from page.logs_page import LogsPage
from page.power_control_page import PowerControlPage
from page.inventory_page import InventoryPage

class Pages:
    def __init__(self, driver):
        self.base = BasePage(driver)
        self.login = LoginPage(driver)
        self.main = MainPage(driver)
        self.logs = LogsPage(driver)
        self.power_control = PowerControlPage(driver)
        self.inventory = InventoryPage(driver)

