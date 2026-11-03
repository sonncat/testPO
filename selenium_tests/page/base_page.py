from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.base_url = 'https://localhost:2443/#/login'
        self.action_chains = ActionChains(self.driver)

    # Метод для открытия страницы
    def open_url(self, url=None):
        if url == None:
            url = self.base_url
        self.driver.get(url)

    # Метод для поиска элемента на странице
    def find_element(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    # Метод для проверки кликабелности элемента на странице
    def element_be_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )
    

    # Метод для клика по элементу
    def click_element(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    # Метод для ввода текста в элемент
    def type(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text
