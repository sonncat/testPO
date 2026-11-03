import pytest
from page.pages import Pages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--guest")
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()


@pytest.fixture
def page(driver):
    return Pages(driver)