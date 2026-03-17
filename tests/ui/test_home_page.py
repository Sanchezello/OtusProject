import pytest
import allure

from selenium import webdriver
from pages.home_page import HomePage
from config import FRONT_URL

@allure.title("Открытие главной страницы магазина")
@allure.description("Проверяем, что главная страница загружается и содержит правильный заголовок")
def test_open_home_page(driver):
    home_page = HomePage(driver)

    with allure.step("Открываем главную страницу"):
        home_page.open()

    with allure.step("Проверяем, что заголовок содержит 'PrestaShop'"):
        title = home_page.get_page_title()
        assert "PrestaShop" in title, f"Ожидался 'PrestaShop' в заголовке, получено: {title}"

    with allure.step("Проверяем видимость логотипа"):
        assert home_page.is_logo_visible(), "Логотип не отображается на главной странице"