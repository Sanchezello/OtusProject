import requests

from config import API_URL


class ApiClient:
    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.session.trust_env = False
        self.base_url = API_URL
        if api_key:
            self.session.auth = (api_key, "")

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        print(f"\n{method.upper()} {url} → {response.status_code}")
        return response

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)

    def post_xml(self, endpoint, xml_data, **kwargs):
        headers = {"Content-Type": "application/xml"}
        return self._request("POST", endpoint, data=xml_data, headers=headers, **kwargs)