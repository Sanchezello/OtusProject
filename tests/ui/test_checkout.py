import pytest
import allure

from selenium import webdriver
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FRONT_URL

@allure.title("Оформление заказа")
@allure.description("Залогиненный пользователь оформляет заказ с оплатой через bank wire")
def test_checkout_order(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    with allure.step("Логинимся"):
        login_page.open_login_page()
        login_page.enter_email("pub@prestashop.com")
        login_page.enter_password("1qaz@WSX3edc")
        login_page.click_sign_in()

    with allure.step("Добавляем товар в корзину"):
        driver.get(FRONT_URL)
        product_page.open_first_product()
        product_page.add_to_cart()
        product_page.proceed_to_checkout_from_modal()

    with allure.step("Переходим к оформлению заказа из корзины"):
        checkout_page.go_to_checkout_from_cart()

    with allure.step("Заполняем адрес (или подтверждаем существующий)"):
        checkout_page.fill_address_step()

    with allure.step("Подтверждаем способ доставки"):
        checkout_page.accept_shipping_method()

    with allure.step("Выбираем оплату через bank wire и подтверждаем заказ"):
        checkout_page.pay_by_bank_wire()

    with allure.step("Проверяем, что заказ оформлен успешно"):
        assert checkout_page.is_order_confirmed(), "Не перешли на страницу подтверждения заказа"