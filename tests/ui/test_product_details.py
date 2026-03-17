import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage


@allure.title("Просмотр деталей товара")
@allure.description("Пользователь кликает по товару и видит его описание")
def test_view_product_details(driver):
    home_page = HomePage(driver)

    with allure.step("Открываем главную"):
        home_page.open()

    with allure.step("Кликаем по первому товару"):
        first_product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "article.product-miniature a.thumbnail"))
        )
        first_product_link.click()

    with allure.step("Проверяем, что открылась страница товара"):
        product_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.h1"))
        )
        assert len(product_name.text) > 0, "Имя товара не отображается"