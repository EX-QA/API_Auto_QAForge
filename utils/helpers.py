import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict


def generate_random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email(domain: str = "test.com") -> str:
    username = generate_random_string(8).lower()
    return f"{username}@{domain}"


def generate_random_phone(prefix: str = "1") -> str:
    return prefix + ''.join(random.choices(string.digits, k=10))


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def date_offset(days: int = 0) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


def random_choice(options: list) -> Any:
    return random.choice(options)


def build_query_params(params: Dict) -> str:
    return "&".join([f"{k}={v}" for k, v in params.items()])
