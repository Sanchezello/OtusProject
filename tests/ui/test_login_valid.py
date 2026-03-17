import pytest
import allure

from selenium import webdriver
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import TXT_URL


@allure.title("Успешный вход в аккаунт")
@allure.description("Пользователь входит с правильным email и паролем, оказывается на главной и видит элемент профиля")
def test_login_valid(driver):
    login_page = LoginPage(driver)

    with allure.step("Открываем страницу входа"):
        login_page.open_login_page()

    with allure.step("Вводим валидные данные"):
        login_page.enter_email("pub@prestashop.com")
        login_page.enter_password("1qaz@WSX3edc")

    with allure.step("Нажимаем 'Sign in'"):
        login_page.click_sign_in()

    with allure.step("Проверяем, что перешли на главную страницу"):
        WebDriverWait(driver, 15).until(
            lambda d: TXT_URL in d.current_url and "/login" not in d.current_url
        )

    with allure.step("Проверяем, что пользователь авторизован (есть ссылка 'My account')"):
        my_account_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'account')]"))
        )
        assert my_account_link.is_displayed(), "Ссылка 'My account' не отображается после входа"