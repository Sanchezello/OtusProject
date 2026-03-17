from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AccountPage:
    def __init__(self, driver):
        self.driver = driver

    def is_account_page(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'logout')]"))
                )
            )
            return True
        except:
            return False

    def go_to_orders(self):
        orders_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/order-history')]"))
        )
        orders_link.click()
		
    def go_to_my_account(self):
        my_account_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'account')]"))
        )
        my_account_link.click()

    def is_logged_in(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'logout')]"))
            )
            return True
        except:
            return False