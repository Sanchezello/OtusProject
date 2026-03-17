import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Customers")
class TestCustomers:

    @allure.title("Получение списка клиентов")
    def test_get_customers_list(self, api_client):
        response = api_client.get("/customers")
        
        with allure.step("Статус код 200"):
            assert response.status_code == 200

        with allure.step("Парсим XML"):
            root = parse_xml(response)

        with allure.step("Проверяем, что корневой элемент — prestashop"):
            assert root.tag == "prestashop", "Ожидался корневой элемент <prestashop>"

        customers = root.find("customers")
        assert customers is not None, "Нет узла <customers>"

        customer_nodes = customers.findall("customer")
        with allure.step(f"Найдено {len(customer_nodes)} клиентов"):
            assert len(customer_nodes) > 0, "Список клиентов пуст"

        first_customer = customer_nodes[0]
        with allure.step("Проверяем наличие атрибута id у первого клиента"):
            assert "id" in first_customer.attrib, "У клиента нет атрибута id"
            assert first_customer.attrib["id"].isdigit(), "ID клиента не число"

    @allure.title("Получение клиента по ID")
    def test_get_customer_by_id(self, api_client):
        response = api_client.get("/customers/1")
        
        with allure.step("Статус код 200"):
            assert response.status_code == 200

        with allure.step("Парсим XML"):
            root = parse_xml(response)

        with allure.step("Проверяем, что это <customer>"):
            assert root.tag == "prestashop", "Ожидался <prestashop>"
            customer = root.find("customer")
            assert customer is not None, "Не найден узел <customer>"

        with allure.step("Проверяем ID клиента"):
            customer_id = customer.find("id")
            assert customer_id is not None, "Нет поля <id>"
            assert customer_id.text == "1", f"Ожидался ID=1, получено {customer_id.text}"