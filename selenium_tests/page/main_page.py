from locators.main_page_locators import MainPageLocators
from page.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.main_page_locators = MainPageLocators()


    def get_username_profile(self):
        user_name = self.get_text(self.main_page_locators.xpath_header_user_auth)
        return(user_name)

    def check_info_is_none(self, locator):
        text = self.get_text(locator=locator)
        info_null = None
        if text == '--':
            info_null = True
        else:
            info_null = False
        return info_null

    def open_main_page(self):
        self.open_url('https://localhost:2443/#/')
        self.find_element(self.main_page_locators.xpath_title_overview)
