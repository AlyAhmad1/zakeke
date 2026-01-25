import traceback
import time
import datetime
import undetected_chromedriver as uc

from src.pages.dashboard import DashboardPage
from src.pages.guest import GuestPage
from src.pages.login import LoginPage

from src.utils.common import (
    wait_with_random_delay,
    save_to_json,
)

def execute_fetch_orders():
    automation_name = "Linkedin Followers Onboarding"
    try:
        # load Chrome extension to use VPN.
        # chrome_options = uc.ChromeOptions()
        # driver = uc.Chrome(version_main=120, options=chrome_options)
        print("------------")
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(
            version_main=143,
            options=options,
            headless=False
        )
        guest_page = GuestPage(driver)
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        logged_in = login_page.login(dashboard_page, guest_page)

        time.sleep(300)

        # Quit chrome session
        driver.quit()

    except Exception as e:
        # send exception alert to slack channel
        exception_data = traceback.format_exc()
        response_data = {'error': 'Server Error'}
        print(exception_data, "<<<<<<<<<")
