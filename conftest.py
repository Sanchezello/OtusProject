import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.api_client import ApiClient
from config import API_KEY


@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # это для докера
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")



    options.binary_location = "/usr/bin/google-chrome"


    driver = webdriver.Chrome(options=options)

    # Небольшая задержка чтобы драйвер инициализировался
    driver.implicitly_wait(10)

    yield driver

    print("\n" + "= " * 50)
    print(f"Test: {request.node.name}")

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        print("+ Тест упал → делаем скриншот")
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"FAIL_{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"X Ошибка при прикреплении скриншота: {e}")

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def api_client():
    return ApiClient(api_key=API_KEY)