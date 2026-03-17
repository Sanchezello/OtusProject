import pytest
import allure

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.account_page import AccountPage


@allure.title("Просмотр истории заказов")
@allure.description("После входа пользователь переходит в историю заказов")
def test_order_history(driver):
    login_page = LoginPage(driver)
    account_page = AccountPage(driver)

    with allure.step("Логинимся"):
        login_page.open_login_page()
        login_page.enter_email("pub@prestashop.com")
        login_page.enter_password("1qaz@WSX3edc")
        login_page.click_sign_in()

    with allure.step("Проверяем, что вошли"):
        assert account_page.is_logged_in(), "Не удалось войти в аккаунт"

    with allure.step("Переходим на страницу 'My account'"):
        account_page.go_to_my_account()

    with allure.step("Переходим в историю заказов"):
        account_page.go_to_orders()

    with allure.step("Проверяем, что попали на страницу истории заказов"):
        WebDriverWait(driver, 15).until(
		    EC.url_contains("order-history")
        )
        assert "order-history" in driver.current_url.lower(), "Не перешли на страницу истории заказов"

    with allure.step("Проверяем, что отображается список заказов"):
        order_table = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-striped"))
        )
        assert order_table.is_displayed(), "Таблица заказов не отображается"