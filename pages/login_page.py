from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FRONT_URL


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = FRONT_URL

    def open_login_page(self):
        self.driver.get(f"{FRONT_URL}/index.php?controller=authentication&back=my-account")

    def open_registration_page(self):
        self.driver.get(f"{FRONT_URL}/registration")
    
    def enter_first_name(self, firstname):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "field-firstname"))
        )
        field.clear()
        field.send_keys(firstname)

    def enter_last_name(self, lastname):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "field-lastname"))
        )
        field.clear()
        field.send_keys(lastname)

    def enter_email(self, email):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "field-email"))
        )
        field.clear()
        field.send_keys(email)

    def enter_password(self, password):
        field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "field-password"))
        )
        field.clear()
        field.send_keys(password)

    def accept_terms_and_privacy(self):
        driver = self.driver

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "customer-form"))
        )

        cgv_label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[.//input[@name='psgdpr']]"))
        )
        cgv_label.click()

        privacy_label = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//label[.//input[@name='customer_privacy']]"))
        )
        privacy_label.click()

        assert driver.find_element(By.NAME, "psgdpr").is_selected(), "'I agree' не выделен"
        assert driver.find_element(By.NAME, "customer_privacy").is_selected(), "'Customer data privacy' не выделен"
        
    def submit_registration(self):
        save_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Save')]"))
        )
        save_button.click()
        
    def click_sign_in(self):
        sign_in_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='submit-login']"))
        )
        sign_in_btn.click()
    
    def get_error_message(self):
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "li.alert.alert-danger"))
            )
            return error.text
        except:
            return ""