import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Categories")
class TestCategories:

    @allure.title("Получение списка категорий")
    def test_get_categories_list(self, api_client):
        response = api_client.get("/categories")
        assert response.status_code == 200
        root = parse_xml(response)
        allure.attach(response.text, "Response XML", allure.attachment_type.XML)
        cats = root.find("categories")
        assert cats is not None, "Нет узла <categories>"
        assert len(cats.findall("category")) > 0, "Список категорий пуст"

    @allure.title("У категории есть имя")
    def test_category_has_name(self, api_client):
        response = api_client.get("/categories")
        assert response.status_code == 200
        root = parse_xml(response)
        cats = root.find("categories")
        assert cats is not None, "Нет узла <categories>"
        for cat in cats.findall("category"):
            if "id" not in cat.attrib:
                continue
            cid = cat.attrib["id"]
            res = api_client.get(f"/categories/{cid}")
            if res.status_code != 200:
                continue
            c = parse_xml(res)
            name = c.find(".//name/language")
            assert name is not None and name.text, f"Имя отсутствует у категории {cid}"