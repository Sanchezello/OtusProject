import pytest
import allure

from selenium import webdriver
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FRONT_URL


@allure.title("Добавление товара в корзину")
@allure.description("Пользователь добавляет товар и переходит в корзину через модальное окно")
def test_add_product_to_cart(driver):
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Открываем главную страницу"):
        driver.get(FRONT_URL)

    with allure.step("Переходим на страницу первого товара"):
        product_page.open_first_product()

    with allure.step("Добавляем товар в корзину"):
        product_page.add_to_cart()

    with allure.step("Нажимаем 'Proceed to checkout' в модальном окне"):
        product_page.proceed_to_checkout_from_modal()

    with allure.step("Проверяем, что перешли в корзину и товар отображается"):
        assert cart_page.is_product_in_cart(), "Товар не отображается в корзине"

    with allure.step("Проверяем название товара в корзине"):
        cart_name = cart_page.get_product_name()
        assert "Hummingbird" in cart_name, f"Ожидался товар с 'Hummingbird', получено: {cart_name}"
        allure.attach(cart_name, name="Товар в корзине", attachment_type=allure.attachment_type.TEXT)