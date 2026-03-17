from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def open_first_product(self):
        first_product = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "article.product-miniature h3 a"))
        )
        first_product.click()

    def add_to_cart(self):
        add_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart"))
        )
        add_btn.click()

    def proceed_to_checkout_from_modal(self):
        checkout_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Proceed to checkout')]"))
        )
        checkout_btn.click()