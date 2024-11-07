from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from classes.site import SauceDemoSite


ROOT_DIR = Path(__file__).resolve().parent
CHROME_DRIVER_PATH = ROOT_DIR / 'chromedriver' / 'chromedriver'
FIREFOX_DRIVER_PATH = ROOT_DIR / 'geckodriver' / 'geckodriver'
EDGE_DRIVER_PATH = ROOT_DIR / 'msedgedriver' / 'msedgedriver'


def chrome_driver():
    service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service)


@pytest.fixture
def setup_driver():
    driver = chrome_driver()
    yield driver
    driver.quit()


@pytest.fixture
def navigate_to_website(setup_driver):
    def _navigate(url):
        setup_driver.get(url)
        return setup_driver
    return _navigate
    

@pytest.fixture
def navigate_to_saucedemo(navigate_to_website):
    url = 'https://www.saucedemo.com/'
    return navigate_to_website(url)


@pytest.fixture
def saucedemo_site(navigate_to_saucedemo):
    return SauceDemoSite(navigate_to_saucedemo)
    