import os
import time
from src.pages.base import BasePage
from src.utils.common import get_random_delay, wait_with_random_delay, save_cookies, load_cookies_in_driver_before_site_load
from src.utils.constants import (ZAKEKE_EMAIL, ZAKEKE_BASE_URL, ZAKEKE_COOKIES_FILENAME, ROOT_PATH, )


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

    def login(self, dashboard_page, guest_page):
        logged_in = False

        # Get the absolute path of the current directory
        current_dir = os.path.abspath(__file__)

        print(".......")
        # Add cookies from file if present
        if os.path.exists(f'{ROOT_PATH}/{ZAKEKE_COOKIES_FILENAME}'):
            load_cookies_in_driver_before_site_load(self.driver, f'{ROOT_PATH}/{ZAKEKE_COOKIES_FILENAME}')
            self.driver.get(ZAKEKE_BASE_URL)
        else:
            self.driver.get(ZAKEKE_BASE_URL)

        random_delay = get_random_delay(10, 20)

        # verify login
        try:
            dashboard_page.wait_for_organization(delay=random_delay)
            logged_in = True
        except Exception as err:
            # not able to access feed page
            print("Exception: ", str(err))

        if not logged_in:
            # Click on Sign In page
            random_delay = get_random_delay(6, 11)
            guest_page.click_sigin_button(delay=random_delay)

            # wait for username field to load
            random_delay = get_random_delay(10, 15)
            self.wait_for_username_field(delay=random_delay)

            # login by giving username and password
            self.enter_email(ZAKEKE_EMAIL)

            # click on login button
            wait_with_random_delay(7, 15)
            self.click_continue_button()

            while True:
                print("---- enter email otp ---")
                random_delay = get_random_delay(10, 15)
                dashboard_page.wait_for_organization(delay=random_delay)
                break

            # save cookies
            # TODO: Save cookies to some cloud storage
            save_cookies(ZAKEKE_EMAIL, self.driver.get_cookies())

            logged_in = True
        else:
            print("Already logged in")

        return logged_in
