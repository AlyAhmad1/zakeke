import os
import time
from src.pages.base import BasePage
from src.utils.common import (
    get_random_delay,
    wait_with_random_delay,
    save_cookies,
    load_cookies_in_driver_before_site_load,
)
from src.utils.constants import (
    ZAKEKE_EMAIL,
    ZAKEKE_LOGIN_URL,
    ZAKEKE_COOKIES_FILENAME,
    ZAKEKE_DASHBOARD_URL,
    ROOT_PATH,
)


class LoginPage(BasePage):
    locators = {
        "email_field": ("name", "email"),
        "continue_button": ("XPATH", "//button[@type='submit']"),
    }

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_email_field(self, delay=5):
        self.wait_for_element(self.email_field, delay)

    def enter_email(self, email):
        self.email_field.clear()
        self.email_field.set_text(email)

    def click_continue_button(self, delay=5):
        self.click_element(self.continue_button, delay)

    def login(self, dashboard_page):
        logged_in = False

        # Add cookies from file if present
        if os.path.exists(f"{ROOT_PATH}/{ZAKEKE_COOKIES_FILENAME}"):
            load_cookies_in_driver_before_site_load(
                self.driver, f"{ROOT_PATH}/{ZAKEKE_COOKIES_FILENAME}"
            )
            self.driver.get(ZAKEKE_DASHBOARD_URL)
            logged_in = True
        else:
            self.driver.get(ZAKEKE_LOGIN_URL)

        if not logged_in:
            random_delay = get_random_delay(10, 15)
            self.wait_for_email_field(delay=random_delay)

            # login by giving username and password
            self.enter_email(ZAKEKE_EMAIL)

            # click on login button
            wait_with_random_delay(3, 5)
            self.click_continue_button()

            while True:
                try:
                    wait_with_random_delay(10, 15)
                    dashboard_page.wait_for_organization(delay=15)
                    break
                except:
                    pass

            wait_with_random_delay(10, 15)

            dashboard_page.click_proceed_button()
            wait_with_random_delay(10, 15)
            # save cookies
            save_cookies(ZAKEKE_COOKIES_FILENAME, self.driver.get_cookies())

            logged_in = True
        else:
            print("Already logged in")

        return logged_in
