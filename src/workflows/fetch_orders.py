import traceback
import time
import datetime
import undetected_chromedriver as uc

from src.pages.dashboard import DashboardPage
from src.pages.order import OrderPage
from src.pages.login import LoginPage

from src.utils.common import (
    wait_with_random_delay,
    save_to_json,
)


def execute_fetch_orders():
    automation_name = "zakake product scraper"
    try:
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(version_main=143, options=options, headless=False)
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        order_page = OrderPage(driver)

        login_page.login(dashboard_page)
        wait_with_random_delay(5, 10)

        order_page.list_today_orders()
        order_page.download_orders()

        # Quit chrome session
        driver.quit()

    except Exception as e:
        exception_data = traceback.format_exc()
        response_data = {"error": "Server Error"}
        print(exception_data, "<<<<<<<<<")
