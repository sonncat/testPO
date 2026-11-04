import pytest
from page.pages import Pages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--guest")
    options.add_argument('ignore-certificate-errors')
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options, service=ChromeService("/usr/bin/chromedriver"))
    
    yield driver
    driver.quit()

@pytest.fixture
def page(driver):
    return Pages(driver)
