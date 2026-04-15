import requests
from typing import Any, Optional


class Assertions:
    @staticmethod
    def assert_status_code(response: requests.Response, expected: int, message: Optional[str] = None):
        actual = response.status_code
        msg = message or f"Expected status code {expected}, got {actual}"
        assert actual == expected, msg

    @staticmethod
    def assert_json_path(response: requests.Response, path: str, expected: Any, message: Optional[str] = None):
        actual = response.json()
        keys = path.split(".")
        for key in keys:
            if isinstance(actual, dict):
                actual = actual.get(key)
            elif isinstance(actual, list):
                actual = actual[int(key)] if key.isdigit() else actual
            else:
                actual = None
                break

        msg = message or f"JSON path '{path}': expected {expected}, got {actual}"
        assert actual == expected, msg

    @staticmethod
    def assert_response_time(response: requests.Response, max_ms: int, message: Optional[str] = None):
        elapsed_ms = response.elapsed.total_seconds() * 1000
        msg = message or f"Response time {elapsed_ms:.2f}ms exceeds limit {max_ms}ms"
        assert elapsed_ms <= max_ms, msg

    @staticmethod
    def assert_header_exists(response: requests.Response, header_name: str, message: Optional[str] = None):
        msg = message or f"Header '{header_name}' not found in response"
        assert header_name in response.headers, msg

    @staticmethod
    def assert_json_value(response: requests.Response, path: str, comparator: str, expected: Any):
        """Flexible comparison: ==, !=, >, <, >=, <=, in"""
        actual = response.json()
        keys = path.split(".")
        for key in keys:
            if isinstance(actual, dict):
                actual = actual.get(key)
            elif isinstance(actual, list):
                actual = actual[int(key)] if key.isdigit() else actual
            else:
                actual = None
                break

        comparators = {
            "==": lambda a, e: a == e,
            "!=": lambda a, e: a != e,
            ">": lambda a, e: a > e,
            "<": lambda a, e: a < e,
            ">=": lambda a, e: a >= e,
            "<=": lambda a, e: a <= e,
            "in": lambda a, e: a in e,
        }
        msg = f"JSON path '{path}': {actual} {comparator} {expected}"
        assert comparators[comparator](actual, expected), msg

    @staticmethod
    def assert_response_contains(response: requests.Response, text: str, message: Optional[str] = None):
        msg = message or f"Response does not contain '{text}'"
        assert text in response.text, msg
