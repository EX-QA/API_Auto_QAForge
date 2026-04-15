import time
from typing import Callable, Optional, Dict, Any
import requests


class HooksManager:
    def __init__(self):
        self._pre_request_hooks: list = []
        self._post_request_hooks: list = []

    def register_pre_request(self, hook: Callable[[str, Dict], None]):
        self._pre_request_hooks.append(hook)

    def register_post_request(self, hook: Callable[[requests.Response], None]):
        self._post_request_hooks.append(hook)

    def execute_pre_request(self, method: str, kwargs: Dict):
        for hook in self._pre_request_hooks:
            hook(method, kwargs)

    def execute_post_request(self, response: requests.Response):
        for hook in self._post_request_hooks:
            hook(response)


class LoggingHook:
    @staticmethod
    def log_request(method: str, kwargs: Dict):
        print(f"[REQUEST] {method.upper()} - {kwargs.get('url', 'unknown')}")

    @staticmethod
    def log_response(response: requests.Response):
        print(f"[RESPONSE] {response.status_code} - {response.elapsed.total_seconds():.3f}s")


def timing_hook(response: requests.Response):
    """Store response time in response object for later assertion"""
    response._elapsed_ms = response.elapsed.total_seconds() * 1000
