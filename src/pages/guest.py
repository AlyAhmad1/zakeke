from src.pages.base import BasePage


class GuestPage(BasePage):
    locators = {
        "signin_button": ("XPATH", "//a[@data-tracking-control-name='guest_homepage-basic_nav-header-signin']")
    }

    def __init__(self, driver):
        super().__init__(driver)

    def click_sigin_button(self, delay=5):
        self.click_element(self.signin_button, delay)
