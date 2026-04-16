import os

import psycopg2
import pytest
from config.settings import get_config
from core.api_client import APIClient
from core.assertions import Assertions
from core.pingcode_client import PingCodeClient
from utils.logger import setup_logger

_pingcode_client_instance = None


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


@pytest.fixture(scope='session')
def pingcode_client(config):
    global _pingcode_client_instance
    client = PingCodeClient(
        server_url=config.pingcode_base_url,
        client_id=config.pingcode_client_id,
        client_secret=config.pingcode_client_secret,
        project_name=config.pingcode_project_name
    )
    _pingcode_client_instance = client
    yield client


def get_pingcode_client():
    return _pingcode_client_instance


@pytest.fixture(scope="session")
def assertions():
    return Assertions()


@pytest.fixture(scope="function")
def logger():
    return setup_logger()


@pytest.fixture(scope="session")
def session_logger():
    return setup_logger("session")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 只关注测试执行阶段（setup/call/teardown 中的 call 阶段）
    if report.when == "call":
        pingcode_client = get_pingcode_client()
        testrun_id = getattr(item, "testcase_dict", None)[getattr(item, "testcase_title", None)]
        if report.outcome == "passed":
            pingcode_client.execute_testcase(run_id=testrun_id, status='passed')
        elif report.outcome == "failed":
            pingcode_client.execute_testcase(run_id=testrun_id, status='failed')
