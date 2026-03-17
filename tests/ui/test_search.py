import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from config import FRONT_URL


@allure.title("Поиск товара по каталогу")
@allure.description("Пользователь вводит запрос и видит результаты поиска")
def test_search_product(driver):
    with allure.step("Открываем главную страницу"):
        driver.get(FRONT_URL)

    with allure.step("Находим поле поиска и вводим запрос"):
        search_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "s"))
        )
        search_input.clear()
        search_input.send_keys("t-shirt")

    with allure.step("Отправляем форму (нажимаем Enter)"):
        search_input.send_keys(Keys.RETURN)

    with allure.step("Проверяем, что перешли на страницу поиска"):
        WebDriverWait(driver, 15).until(
            EC.url_contains("/search")
        )
        assert "search" in driver.current_url.lower(), "Не перешли на страницу поиска"

    with allure.step("Проверяем, что есть хотя бы один товар"):
        products = driver.find_elements(By.CSS_SELECTOR, ".js-product, .product-miniature")
        assert len(products) > 0, "Нет ни одного товара в результатах поиска"

    with allure.step("Проверяем, что название товара содержит 't-shirt'"):
        found = False
        for product in products:
            try:
                title_element = product.find_element(By.CSS_SELECTOR, ".product-title a")
                title_text = title_element.text.strip().lower()
                if "t-shirt" in title_text:
                    found = True
                    break
            except:
                continue

        assert found, "Ни один товар не содержит 't-shirt' в названии"