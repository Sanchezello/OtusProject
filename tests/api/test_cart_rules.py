import allure
import pytest

from xml.etree import ElementTree as ET


def parse_xml(response):
    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        raise AssertionError(f"Не удалось распарсить XML: {e}")


@allure.feature("API: Cart Rules")
class TestCartRules:

    @allure.title("Получение списка правил корзины")
    def test_get_cart_rules_list(self, api_client):
        response = api_client.get("/cart_rules")
        with allure.step("Статус код 200"):
            assert response.status_code == 200
        root = parse_xml(response)
        allure.attach(response.text, "Response XML", allure.attachment_type.XML)
        rules = root.find("cart_rules")
        assert rules is not None, "Нет узла <cart_rules>"

    @allure.title("Правило имеет валидный процент скидки")
    def test_cart_rule_has_valid_reduction_percent(self, api_client):
        response = api_client.get("/cart_rules?display=[id,reduction_percent]")
        assert response.status_code == 200
        root = parse_xml(response)
        for rule in root.find("cart_rules").findall("cart_rule"):
            res = api_client.get(f"/cart_rules/{rule.attrib['id']}")
            r = parse_xml(res)
            percent = r.find(".//reduction_percent")
            if percent is not None and percent.text:
                try:
                    val = float(percent.text)
                    assert 0 <= val <= 100, f"Скидка вне диапазона: {val}%"
                except:
                    assert False, f"reduction_percent не число: {percent.text}"

    @allure.title("Правило активно (active=1)")
    def test_cart_rule_is_active(self, api_client):
        response = api_client.get("/cart_rules?filter[active]=1")
        assert response.status_code == 200
        root = parse_xml(response)
        rules = root.find("cart_rules").findall("cart_rule")
        for r in rules:
            res = api_client.get(f"/cart_rules/{r.attrib['id']}")
            rule = parse_xml(res)
            active = rule.find(".//active")
            assert active is not None and active.text == "1", "Правило не активно"

    @allure.title("Фильтр: правила по коду")
    def test_filter_cart_rules_by_code(self, api_client):
        response = api_client.get("/cart_rules?filter[code]=WELCOME")
        assert response.status_code == 200
        root = parse_xml(response)
        rules = root.find("cart_rules").findall("cart_rule")
        for r in rules:
            res = api_client.get(f"/cart_rules/{r.attrib['id']}")
            rule = parse_xml(res)
            code = rule.find(".//code")
            assert code is not None
            assert "WELCOME" in code.text, f"Код не содержит WELCOME: {code.text}"