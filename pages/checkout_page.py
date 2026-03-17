from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_checkout_from_cart(self):
        proceed_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'checkout') or contains(text(), 'Proceed to checkout')]"))
        )
        proceed_btn.click()

    def fill_address_step(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "js-address-item"))
            )
            
            # radio с value="5"
            address_radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='id_address_delivery'][value='5']")
            address_radio.click()
            
            # Continue
            continue_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "confirm-addresses"))
            )
            continue_btn.click()
        except Exception as e:
            print(f"Ошибка при выборе адреса: {e}")
            raise
    
    def accept_shipping_method(self):
        try:
            # Ждём загрузки
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "delivery-options"))
            )
            
            # Кликаем по лейблу
            shipping_label = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='delivery_option_2']"))
            )
            shipping_label.click()
            
            # Continue
            continue_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "confirmDeliveryOption"))
            )
            continue_btn.click()
        except Exception as e:
            print(f"Ошибка при выборе доставки: {e}")
            raise
    
    def pay_by_bank_wire(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "checkout-payment-step"))
        )
        
        try:
            bankwire_label = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='payment-option-3']"))
            )
            bankwire_label.click()
        except:
            first_payment_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[starts-with(@for, 'payment-option-')]"))
            )
            first_payment_option.click()
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "payment-option-3-additional-information"))
        )
        
        # Ставим галочку
        try:
            terms_label = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='conditions_to_approve[terms-and-conditions]']"))
            )
            terms_label.click()
        except:
            checkbox = self.driver.find_element(By.ID, "conditions_to_approve[terms-and-conditions]")
            self.driver.execute_script("arguments[0].click();", checkbox)
        
        # Подтверждаем
        place_order_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#payment-confirmation button:not([disabled])"))
        )
        place_order_btn.click()

    def is_order_confirmed(self):
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("/order-confirmation")
        )
        return "order-confirmation" in self.driver.current_url