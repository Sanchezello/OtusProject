import pytest
import allure
import time

from selenium import webdriver
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import TXT_URL


@allure.title("Регистрация нового пользователя")
@allure.description("Пользователь заполняет форму регистрации и создаёт аккаунт")
def test_register_new_user(driver):
    login_page = LoginPage(driver)
    account_page = AccountPage(driver)

    with allure.step("Открываем страницу регистрации"):
        login_page.open_registration_page()

    with allure.step("Заполняем персональные данные"):
        login_page.enter_first_name("Kotik")
        login_page.enter_last_name("White")

    with allure.step("Указываем контактные данные"):
        unique_email = f"kotik2.white@prestashop.com"
        login_page.enter_email(unique_email)
        login_page.enter_password("1qaz@WSX3edc")

    with allure.step("Принимаем условия и политику конфиденциальности"):
        login_page.accept_terms_and_privacy()

    with allure.step("Отправляем форму"):
        login_page.submit_registration()

    with allure.step("Проверяем, что перешли на главную страницу"):
        WebDriverWait(driver, 15).until(
            lambda d: TXT_URL in d.current_url and "/registration" not in d.current_url
        )

    with allure.step("Проверяем, что пользователь авторизован"):
        assert account_page.is_logged_in(), "Пользователь не авторизован после регистрации"