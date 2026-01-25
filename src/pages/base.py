from abc import ABC

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumpagefactory.Pagefactory import PageFactory


class BasePage(ABC, PageFactory):
    locators = {}

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, element, delay):
        _locator_data = element._locator
        locator = (self.TYPE_OF_LOCATORS[_locator_data[0].lower()], _locator_data[1])

        _element = WebDriverWait(self.driver, delay).until(
            EC.presence_of_element_located(locator)
        )

    def scroll_to_element(self, element):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    def click_element(self, element, delay):
        self.wait_for_element(element, delay)
        self.scroll_to_element(element)
        element.click()

    def scroll_to_page_top(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollTop);")

    def scroll_to_page_end(self, loop=False):
        if loop:
            pass
        else:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

    def get_elements(self, locator_type, locator):
        elements = self.driver.find_elements(locator_type, locator)
        return elements
