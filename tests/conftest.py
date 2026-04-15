import os

import psycopg2
import pytest
from config.settings import get_config
from core.api_client import APIClient
from core.assertions import Assertions
from utils.logger import setup_logger


@pytest.fixture(scope="session")
def config():
    return get_config()


@pytest.fixture(scope="session")
def api_client(config):
    client = APIClient(
        base_url=config.base_url,
        timeout=config.timeout,
        verify_ssl=config.verify_ssl
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def assertions():
    return Assertions()


@pytest.fixture(scope="function")
def logger():
    return setup_logger()


@pytest.fixture(scope="session")
def session_logger():
    return setup_logger("session")



