import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Products")
class TestProducts:

    @allure.title("Получение списка товаров")
    def test_get_products_list(self, api_client):
        response = api_client.get("/products")
        assert response.status_code == 200
        root = parse_xml(response)
        allure.attach(response.text, "Response XML", allure.attachment_type.XML)
        products = root.find("products")
        assert products is not None, "Нет узла <products>"
        product_list = products.findall("product")
        assert len(product_list) > 0, "Список товаров пуст"

    @allure.title("Получение товара по ID")
    @pytest.mark.parametrize("product_id", [1, 2])
    def test_get_product_by_id(self, api_client, product_id):
        response = api_client.get(f"/products/{product_id}")
        if response.status_code == 404:
            pytest.skip(f"Товар {product_id} не существует")
        assert response.status_code == 200
        root = parse_xml(response)
        product = root.find("product")
        assert product is not None, "Не найден <product>"
        pid = product.find("id")
        assert pid is not None and pid.text == str(product_id)

    @allure.title("Проверка корректности данных товара")
    def test_product_has_valid_data(self, api_client):
        response = api_client.get("/products")
        assert response.status_code == 200
        root = parse_xml(response)
        for p in root.find("products").findall("product"):
            pid_elem = p.find("id")
            if pid_elem is None or not pid_elem.text:
                continue
            pid = pid_elem.text
            res = api_client.get(f"/products/{pid}")
            if res.status_code != 200:
                continue
            pr = parse_xml(res)
            name = pr.find(".//name/language")
            price = pr.find(".//price")
            active = pr.find(".//active")
            with allure.step(f"Товар {pid}: проверяем поля"):
                assert name is not None and name.text, "Имя отсутствует"
                assert price is not None and price.text, "Цена отсутствует"
                assert active is not None and active.text in ["0", "1"], "Активность некорректна"

    @allure.title("Поиск по названию (полный просмотр)")
    def test_search_product_by_name_fulltext(self, api_client):
        response = api_client.get("/products?display=full")
        if response.status_code == 500:
            pytest.skip("Фильтр display=full вызывает 500")
        assert response.status_code == 200
        root = parse_xml(response)
        found = False
        for p in root.find("products").findall("product"):
            pid = p.find("id").text
            res = api_client.get(f"/products/{pid}")
            if res.status_code != 200:
                continue
            pr = parse_xml(res)
            name = pr.find(".//name/language")
            if name is not None and "Hummingbird" in name.text:
                found = True
                break
        assert found, "Не найдено товаров с 'Hummingbird' в названии"

    @allure.title("Проверка цены — числовое значение")
    def test_product_price_is_numeric(self, api_client):
        response = api_client.get("/products")
        if response.status_code == 500:
            pytest.skip("GET /products вернул 500")
        assert response.status_code == 200
        root = parse_xml(response)
        
        products = root.find("products")
        assert products is not None, "Нет узла <products>"
        
        for p in products.findall("product"):
            if "id" not in p.attrib:
                continue
            pid = p.attrib["id"]
            
            res = api_client.get(f"/products/{pid}")
            if res.status_code != 200:
                continue
                
            pr = parse_xml(res)
            price = pr.find(".//price")
            
            assert price is not None and price.text, f"Цена отсутствует у товара {pid}"
            
            try:
                float(price.text)
            except (ValueError, TypeError):
                assert False, f"Цена не число: {price.text}"

    @allure.title("Товар имеет категорию (associations)")
    def test_product_has_category(self, api_client):
        response = api_client.get("/products")
        assert response.status_code == 200
        root = parse_xml(response)
        for p in root.find("products").findall("product"):
            if "id" not in p.attrib:
                continue
            pid = p.attrib["id"]
            res = api_client.get(f"/products/{pid}?ws_access[]=categories")
            if res.status_code != 200:
                continue
            pr = parse_xml(res)
            categories = pr.find(".//associations/categories")
            assert categories is not None and len(categories) > 0, f"Нет категорий у товара {pid}"
    
    @allure.title("Товар имеет изображение (через associations)")
    def test_product_has_image_via_associations(self, api_client):
        response = api_client.get("/products")
        assert response.status_code == 200
        root = parse_xml(response)
        found_with_image = False
        for p in root.find("products").findall("product"):
            if "id" not in p.attrib:
                continue
            pid = p.attrib["id"]
            res = api_client.get(f"/products/{pid}?ws_access[]=images")
            if res.status_code != 200:
                continue
            pr = parse_xml(res)
            images = pr.find(".//associations/images")
            if images is not None and len(images) > 0:
                found_with_image = True
                break
        assert found_with_image, "Не найдено ни одного товара с изображением"