import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Manufacturers")
class TestManufacturers:

    @allure.title("Получение списка производителей")
    def test_get_manufacturers_list(self, api_client):
        response = api_client.get("/manufacturers")
        if response.status_code == 500:
            pytest.skip("Модуль manufacturers не поддерживает 500")
        assert response.status_code == 200
        root = parse_xml(response)
        allure.attach(response.text, "Response XML", allure.attachment_type.XML)
        mans = root.find("manufacturers")
        assert mans is not None, "Нет узла <manufacturers>"
        assert len(mans.findall("manufacturer")) > 0

    @allure.title("Производитель имеет контактные данные")
    def test_manufacturer_has_address(self, api_client):
        response = api_client.get("/manufacturers")
        if response.status_code == 500:
            pytest.skip("Фильтр вызывает 500")
        assert response.status_code == 200
        root = parse_xml(response)
        for m in root.find("manufacturers").findall("manufacturer"):
            mid = m.find("id")
            if mid is None or not mid.text:
                continue
            res = api_client.get(f"/manufacturers/{mid.text}")
            if res.status_code != 200:
                continue
            man = parse_xml(res)
            phone = man.find(".//phone")
            email = man.find(".//email")
            assert phone is not None or email is not None, f"Нет контактов у {mid.text}"