from locators.logs_page_locators import LogsPageLocators
from page.base_page import BasePage


class LogsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logs_page_locators = LogsPageLocators()

    def open_logs_page(self):
        self.open_url('https://localhost:2443/#/logs/event-logs')
        self.find_element(self.logs_page_locators.xpath_logs_title)

    # Метод берет локатор заглушку из таблицы, если находит, то возвращает True, т.к таблица пустая
    # False если таблица не пустая
    def check_logs_is_none_in_table(self):
        table_none = None
        try:
            self.find_element(self.logs_page_locators.xpath_table_none_logs)
        except:
            table_none = False
        else:
            table_none = True
        return table_none