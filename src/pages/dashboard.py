from src.pages.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.common import (
    wait_with_random_delay
)


class DashboardPage(BasePage):
    locators = {
        "organization": ("XPATH", "//h5['Your organizations']"),
        "proceed_button": ("XPATH", "//a[contains(@class,'sc-')]"),
    }

    def __init__(self, driver):
        super().__init__(driver)

    def click_proceed_button(self, delay=5):
        self.click_element(self.proceed_button, delay)


    def wait_for_organization(self, delay=5):
        self.wait_for_element(self.organization, delay)
        self.click_proceed_button()
