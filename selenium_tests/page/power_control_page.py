from locators.power_page_locators import PowerControlLocators 
from page.base_page import BasePage


class PowerControlPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.power_control_locators = PowerControlLocators()

    def open_control_page(self):
        self.open_url('https://localhost:2443/#/operations/server-power-operations')
        title_text = self.get_text(self.power_control_locators.xpath_power_control_title)
        assert title_text == 'Server power operations', 'Открылась не страница управления питанием'

    def power_control_status(self):
        status = self.get_text(self.power_control_locators.xpath_power_status)
        return status

    def shutdown_server(self):
        self.action_chains.move_to_element(self.find_element(self.power_control_locators.xpath_button_shut_down)).perform()
        self.click_element(self.power_control_locators.xpath_button_shut_down)
        self.find_element(self.power_control_locators.xpath_modal_server_shut_down)
        self.click_element(self.power_control_locators.xpath_modal_shut_down_button)
