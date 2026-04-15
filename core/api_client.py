import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin


class APIClient:
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        verify_ssl: bool = True,
        headers: Optional[Dict[str, str]] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> requests.Response:
        url = self._build_url(path)
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify_ssl)
        return self.session.request(method, url, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def set_header(self, key: str, value: str):
        self.session.headers[key] = value

    def remove_header(self, key: str):
        self.session.headers.pop(key, None)

    def close(self):
        self.session.close()
