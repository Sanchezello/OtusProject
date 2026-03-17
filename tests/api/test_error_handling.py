import allure
import pytest


@allure.feature("API: Error Handling")
class TestErrorHandling:

    @allure.title("Запрос к несуществующему ресурсу")
    def test_404_not_found(self, api_client):
        response = api_client.get("/nonexistent-endpoint")
        with allure.step("Ожидаю 400 или 404"):
            assert response.status_code in [400, 404], f"Ожидался 400 или 404, получено {response.status_code}"
        allure.attach(response.text, "Response", allure.attachment_type.TEXT)
    
    @allure.title("POST с неверным Content-Type")
    def test_post_wrong_content_type(self, api_client):
        response = api_client.post(
            "/customers",
            data="<invalid>",
            headers={"Content-Type": "text/plain"}
        )
        with allure.step("Ожидаю 400, 500 или 415"):
            assert response.status_code in [400, 500, 415], "Сервер должен отклонить запрос"
        allure.attach(response.text, "Response", allure.attachment_type.TEXT)