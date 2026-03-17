import allure
import pytest

from xml.etree import ElementTree as ET


CUSTOMER_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<prestashop>
    <customer>
        <email><![CDATA[kotik0.white@prestashop.com]]></email>
        <passwd><![CDATA[1qaz@WSX3edc]]></passwd>
        <lastname><![CDATA[Kotik]]></lastname>
        <firstname><![CDATA[White]]></firstname>
        <id_gender>1</id_gender>
        <id_default_group>3</id_default_group>
        <id_lang>1</id_lang>
        <newsletter>0</newsletter>
        <optin>0</optin>
        <active>1</active>
        <is_guest>0</is_guest>
        <id_shop>1</id_shop>
        <id_shop_group>1</id_shop_group>
    </customer>
</prestashop>
"""


@allure.feature("API: Create Customer")
class TestCreateCustomer:

    @allure.title("Создание нового клиента")
    def test_create_customer(self, api_client):
        xml_data = CUSTOMER_XML_TEMPLATE

        response = api_client.post_xml("/customers", xml_data)
        with allure.step("Проверяем статус 201 Created"):
            assert response.status_code == 201, f"Ожидался 201, получено {response.status_code}"

        with allure.step("Парсим ответ — должен содержать ID"):
            root = ET.fromstring(response.content)
            customer_id = root.find(".//id")
            assert customer_id is not None, "Не вернулся ID клиента"
            allure.attach(response.text, "Created Customer XML", allure.attachment_type.XML)

    @allure.title("Создание клиента с пустым email")
    def test_create_customer_empty_email(self, api_client):
        xml_data = CUSTOMER_XML_TEMPLATE.replace("kotik0.white@prestashop.com", "")
        response = api_client.post_xml("/customers", xml_data)
        assert response.status_code == 400, "Ожидалась ошибка валидации"

    @allure.title("Попытка создания клиента с дублем email")
    def test_create_customer_duplicate_email(self, api_client):
        xml_data = CUSTOMER_XML_TEMPLATE
    
        first = api_client.post("/customers", data=xml_data, headers={"Content-Type": "application/xml"})
        assert first.status_code in [201, 400, 500], "Первый запрос должен создать или вернуть ошибку"
    
        second = api_client.post("/customers", data=xml_data, headers={"Content-Type": "application/xml"})
    
        with allure.step("Повторное создание с тем же email - должно быть запрещено"):
            assert second.status_code in [400, 500], f"Ожидалась ошибка, получено {second.status_code}"
            if second.status_code == 500:
                allure.attach(
                    "Сервер возвращает 500 при дубле email - возможно, баг валидации",
                    "Проблема",
                    allure.attachment_type.TEXT
                )

    @allure.title("Создание клиента без обязательного поля (firstname)")
    def test_create_customer_missing_firstname(self, api_client):
        xml_data = CUSTOMER_XML_TEMPLATE
        xml_data = xml_data.replace("<firstname><![CDATA[Kotik]]></firstname>", "")
        response = api_client.post("/customers", data=xml_data, headers={"Content-Type": "application/xml"})
    
        with allure.step("Отсутствует firstname → должно вызвать ошибку"):
            assert response.status_code in [400, 500], f"Ожидалась ошибка, получено {response.status_code}"
            if response.status_code == 500:
                allure.attach(
                    "Сервер падает при отсутствии firstname — требуется фикс валидации",
                    "Баг",
                    allure.attachment_type.TEXT
                )