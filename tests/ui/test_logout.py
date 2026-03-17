import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.account_page import AccountPage


@allure.title("Выход из аккаунта")
@allure.description("Пользователь выходит из личного кабинета и больше не имеет доступа")
def test_logout(driver):
    login_page = LoginPage(driver)
    account_page = AccountPage(driver)

    with allure.step("Логинимся"):
        login_page.open_login_page()
        login_page.enter_email("pub@prestashop.com")
        login_page.enter_password("1qaz@WSX3edc")
        login_page.click_sign_in()

    with allure.step("Проверяем, что вошли в аккаунт (есть 'Sign out')"):
        assert account_page.is_account_page(), "Не удалось войти в аккаунт"

    with allure.step("Нажимаем 'Sign out'"):
        sign_out_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'logout')]"))
        )
        sign_out_btn.click()

    with allure.step("Проверяем, что появилась кнопка 'Sign in' (пользователь вышел)"):
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Sign in')]"))
        )

    with allure.step("Проверяем, что кнопка 'Sign out' исчезла"):
        WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'logout')]"))
        )