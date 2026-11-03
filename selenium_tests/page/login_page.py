from locators.login_page_locators import LoginPageLocators
from page.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.login_page_locators = LoginPageLocators()


    def fill_login(self, login):
        self.type(locator=self.login_page_locators.xpath_login, text=login)

    def fill_password(self, password):
        self.type(locator=self.login_page_locators.xpath_password, text=password)

    def click_login_button(self):
        self.element_be_clickable(self.login_page_locators.xpath_login_button)
        self.click_element(self.login_page_locators.xpath_login_button)

    def check_login_alert(self):
        self.find_element(self.login_page_locators.xpath_login_alert_error)
        login_text_error = self.get_text(self.login_page_locators.xpath_login_error_text)
        return(login_text_error)

    def full_login_root(self):
        self.open_url()
        self.fill_login("root")
        self.fill_password("0penBmc")
        self.click_login_button()

        

