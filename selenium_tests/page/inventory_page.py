from page.base_page import BasePage
from locators.inventory_page_locators import InventoryPageLocators


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.inventory_page_locators = InventoryPageLocators()

    def count_item_processor(self):
        item_text = self.get_text(self.inventory_page_locators.xpath_count_item_processor)
        count_text = item_text[:item_text.find(' ')]
        count_processor = int(count_text)
        return count_processor

    def scroll_to_inventory_table(self):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(self.inventory_page_locators.xpath_table_processor))

    def open_inventory_page(self):
        self.open_url('https://localhost:2443/#/hardware-status/inventory')
        title_text = self.get_text(self.inventory_page_locators.xpath_inventory_title)
        assert title_text == 'Inventory and LEDs', 'Страница Inventory and LEDs не открылась'