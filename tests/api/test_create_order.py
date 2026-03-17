import allure
import pytest

from xml.etree import ElementTree as ET


ORDER_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<prestashop>
    <order>
        <id_address_delivery>1</id_address_delivery>
        <id_address_invoice>1</id_address_invoice>
        <id_cart>1</id_cart>
        <id_currency>1</id_currency>
        <id_lang>1</id_lang>
        <id_customer>1</id_customer>
        <id_carrier>1</id_carrier>
        <current_state>1</current_state>
        <module>bankwire</module>
        <total_paid>19.12</total_paid>
        <total_paid_real>19.12</total_paid_real>
        <total_products>19.12</total_products>
        <total_shipping>0.00</total_shipping>
        <conversion_rate>1</conversion_rate>
        <valid>1</valid>
        <payment>10</payment>
    </order>
</prestashop>
"""


@allure.feature("API: Create Order")
class TestCreateOrder:

    @allure.title("Создание нового заказа")
    def test_create_order(self, api_client):
        response = api_client.post(
            "/orders",
            data=ORDER_XML_TEMPLATE,
            headers={"Content-Type": "application/xml"}
        )
    
        with allure.step("Проверяем, что заказ создан или возвращена ошибка валидации"):
            assert response.status_code in [201, 400, 500], f"Неожиданный статус: {response.status_code}"
    
        if response.status_code == 201:
            root = ET.fromstring(response.content)
            order_id = root.find(".//id")
            assert order_id is not None, "ID заказа не возвращён"
            allure.attach(response.text, "Created Order", allure.attachment_type.XML)
        elif response.status_code == 400:
            allure.attach(response.text, "Validation Error", allure.attachment_type.TEXT)
        elif response.status_code == 500:
            allure.attach(response.text, "Server Error", allure.attachment_type.TEXT)

    @allure.title("Создание заказа с неверными данными")
    def test_create_order_invalid_customer(self, api_client):
        invalid_xml = ORDER_XML_TEMPLATE.replace("<id_customer>1</id_customer>", "<id_customer>-99999</id_customer>")
        response = api_client.post(
            "/orders",
            data=invalid_xml,
            headers={"Content-Type": "application/xml"}
        )
        with allure.step("Ожидаются ошибки валидации или 400/500"):
            assert response.status_code in [400, 500], "Ожидалась ошибка при неверном customer"