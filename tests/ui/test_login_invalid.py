import pytest
import allure

from selenium import webdriver
from pages.login_page import LoginPage


@allure.title("Вход с неверным паролем")
@allure.description("Система показывает ошибку при неправильном пароле")
def test_login_invalid_password(driver):
    login_page = LoginPage(driver)

    with allure.step("Открываем страницу входа"):
        login_page.open_login_page()

    with allure.step("Вводим email и неверный пароль"):
        login_page.enter_email("pub@prestashop.com")
        login_page.enter_password("1qaz@WSX3edcc")

    with allure.step("Нажимаем 'Sign in'"):
        login_page.click_sign_in()

    with allure.step("Проверяем сообщение об ошибке"):
        error = login_page.get_error_message()
        assert "authentication failed" in error.lower(), f"Ожидалась ошибка, получено: {error}"