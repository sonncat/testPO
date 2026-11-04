from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


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

    # Метод для проверки кликабельности элемента на странице
    def element_be_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # Метод для ввода текста в элемент
    def type(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def click_element(self, locator):
        if isinstance(locator, tuple):
            by, value = locator
        else:
            by, value = By.XPATH, locator

        element = self.wait.until(
            EC.presence_of_element_located((by, value))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)