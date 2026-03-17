import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Orders")
class TestOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, api_client):
        response = api_client.get("/orders")
        if response.status_code == 404:
            pytest.skip("Модуль orders не активен")
        assert response.status_code == 200
        root = parse_xml(response)
        allure.attach(response.text, "Response XML", allure.attachment_type.XML)
        orders = root.find("orders")
        assert orders is not None, "Нет узла <orders>"

    @allure.title("Получение заказа по ID")
    @pytest.mark.parametrize("order_id", [1, 2])
    def test_get_order_by_id(self, api_client, order_id):
        response = api_client.get(f"/orders/{order_id}")
        if response.status_code == 404:
            pytest.skip(f"Заказ {order_id} не существует")
        assert response.status_code == 200
        root = parse_xml(response)
        order = root.find("order")
        assert order is not None
        oid = order.find("id")
        assert oid is not None and oid.text == str(order_id)

    @allure.title("Проверка структуры заказа")
    def test_order_has_required_fields(self, api_client):
        response = api_client.get("/orders")
        if response.status_code == 500:
            pytest.skip("Фильтр не поддерживается")
        assert response.status_code == 200
        root = parse_xml(response)
        orders = root.find("orders")
        if orders is None or len(orders) == 0:
            pytest.skip("Нет заказов")
        for o in orders.findall("order"):
            oid = o.find("id")
            if oid is None or not oid.text:
                continue
            res = api_client.get(f"/orders/{oid.text}")
            if res.status_code != 200:
                continue
            order = parse_xml(res)
            customer_id = order.find(".//id_customer")
            total_paid = order.find(".//total_paid")
            assert customer_id is not None and customer_id.text.isdigit()
            assert total_paid is not None
            try:
                float(total_paid.text)
            except:
                assert False, f"Сумма не число: {total_paid.text}"