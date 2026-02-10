from src.pages.base import BasePage
from datetime import datetime
from src.utils.constants import ZAKEKE_ORDER_URL
from src.utils.common import (
    wait_with_random_delay,
    generate_log,
    read_logs,
)
from selenium.webdriver.common.by import By


class OrderPage(BasePage):
    locators = {
        "from_date_field": ("xpath", "(//input[@type='datetime-local'])[1]"),
        "today_date": ("xpath", "//button[contains(text(), 'Today')]"),
    }

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_from_date_field(self, delay=5):
        self.wait_for_element(self.from_date_field, delay)

    def enter_current_date(self):
        now = datetime.now().strftime("%Y-%m-%dT00:00")
        print(now, "<<<<<<<<<<<<<<<")

        self.click_element(self.from_date_field, 10)
        wait_with_random_delay(5, 10)
        # self.click_element(self.today_date, 10)

        # self.click_element(self.from_date_field, 10)
        # wait_with_random_delay(5, 10)

        # self.from_date_field.clear()
        # # Set value using JavaScript
        # self.driver.execute_script(
        #     "arguments[0].setAttribute('value', arguments[1]);",
        #     self.from_date_field,
        #     now
        # )

    def list_today_orders(self):
        self.driver.get(ZAKEKE_ORDER_URL)
        wait_with_random_delay(5, 10)

        self.wait_for_from_date_field()
        self.enter_current_date()
        wait_with_random_delay(5, 10)

    def download_orders(self):
        for i in range(3):
            self.driver.find_element(By.XPATH, f'//li[@id="tab:r0:{i}"]').click()
            wait_with_random_delay(3, 5)

            order_panel = self.driver.find_element(
                By.XPATH, f'//div[@id="panel:r0:{i}"]'
            )
            wait_with_random_delay(3, 5)

            try:
                main_order_lst = order_panel.find_element(
                    By.CSS_SELECTOR, 'div[columns*="45px"]'
                )
            except Exception as e:
                main_order_lst = order_panel.find_element(
                    By.CSS_SELECTOR, 'div[columns*="26%"]'
                )

            order_divs = main_order_lst.find_elements(By.XPATH, "./div")

            tab_logs = set(read_logs(f"r0_{i}"))

            order_numbers = set()
            # Skip the first div (header) and iterate over the rest
            for index, div in enumerate(order_divs[1:], start=1):
                try:
                    print(f"\nProcessing row {index}...")

                    # Find all span elements within this div
                    spans = div.find_elements(By.TAG_NAME, "span")

                    if spans:
                        if i == 2:
                            order_number = spans[1].text
                            last_span = spans[-1].find_element(By.TAG_NAME, "svg")
                        else:
                            order_number = spans[2].text
                            last_span = spans[-1]
                        if order_number in tab_logs:
                            break

                        try:
                            last_span.click()
                            print(f"✓ Clicked last span in row {index}")
                            wait_with_random_delay(3, 5)
                            if i == 2:
                                self.driver.find_element(
                                    By.XPATH, "//button[text()='Zip file']"
                                ).click()
                                wait_with_random_delay(3, 5)
                                div.find_elements(By.TAG_NAME, "span")[-1].find_element(
                                    By.TAG_NAME, "svg"
                                ).click()
                            else:
                                self.driver.find_element(
                                    By.XPATH, "//span[text()='from here']"
                                ).click()
                                wait_with_random_delay(3, 5)
                                last_span.click()
                            order_numbers.add(order_number)

                        except Exception as e:
                            # If regular click fails, try JavaScript click
                            self.driver.execute_script(
                                "arguments[0].click();", last_span
                            )
                            print(
                                f"✓ Clicked last span in row {index} (using JavaScript)"
                            )
                    else:
                        print(f"⚠ No spans found in row {index}")
                except Exception as e:
                    print(f"✗ Error processing row {index}: {str(e)}")
                    continue

                wait_with_random_delay(3, 5)

                # break
            generate_log(f"r0_{i}", order_numbers)
            wait_with_random_delay(3, 5)

            # break
