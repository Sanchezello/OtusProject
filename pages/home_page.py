from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FRONT_URL


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = FRONT_URL

    def open(self):
        """Открыть главную страницу"""
        self.driver.get(self.url)

    def get_page_title(self):
        """Получить заголовок страницы"""
        return self.driver.title

    def is_logo_visible(self):
        """Проверить видимость логотипа"""
        try:
            logo = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "img.logo"))
            )
            return logo.is_displayed()
        except:
            return False

    def click_sign_in(self):
        """Нажать кнопку 'Sign in'"""
        sign_in_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign in')]"))
        )
        sign_in_btn.click()

    def get_alert_message(self):
        """Получить текст сообщения об ошибке (если есть)"""
        try:
            alert = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-danger"))
            )
            return alert.text
        except:
            return ""