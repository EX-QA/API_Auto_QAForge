import os

import psycopg2
import pytest

from business.user_flow import UserFlow
from core.assertions import Assertions
from data.data_loader import load_test_data
from utils.helpers import generate_random_email, generate_random_string


class TestUserAPI:

    @pytest.fixture(scope='class', autouse=True)
    def create_pingcode_testplan(self, pingcode_client):
        return pingcode_client.create_plan_and_add_testcases(suite_name='注册登录模块',
                                                             plan_name='api_auto_用户注册',
                                                             assignee_name='huan')

    @pytest.fixture(autouse=True)
    def setup(self, api_client, create_pingcode_testplan):
        self.client = api_client
        self.assertions = Assertions()
        self.user_flow = UserFlow(api_client)
        self.testcase_register = create_pingcode_testplan
        print('setup')

    @pytest.mark.parametrize("testcases", load_test_data('register_cases.yaml')[0]['Register'])
    def test_user_register(self, testcases, request):
        """注册功能测试"""
        # response = self.user_flow.register_user(username=username, email=email, password=password)
        # self.assertions.assert_status_code(response, expected_status_code)
        # 测试函数可以通过 request fixture 获取当前节点（node），然后给它添加任意属性。在钩子中通过同一个 item.node 读取即可。
        request.node.testcase_title = testcases['title']
        request.node.testcase_dict = self.testcase_register
        if testcases['type'] == 'success':
            response = self.user_flow.register_user(username=testcases['request_data']['username'],
                                                    email=testcases['request_data']['email'],
                                                    password=testcases['request_data']['password'])
            print('success')
            Assertions.assert_status_code(response, testcases['response_code'])
            Assertions.assert_json_value(response, "username", "==", testcases['response_body']['username'])
            Assertions.assert_json_value(response, "email", "==", testcases['response_body']['email'])
            # Assertions.assert_json_value(response, "id", ">", 0)
            Assertions.assert_json_value(response, 'role', "==", testcases['response_body']['role'])
            # Assertions.assert_json_value(response, 'createdAt', '>', 0)
        elif testcases['type'] in ['field_null', 'duplicate_error']:
            response = self.user_flow.register_user(username=testcases['request_data']['username'],
                                                    email=testcases['request_data']['email'],
                                                    password=testcases['request_data']['password'])
            Assertions.assert_status_code(response, testcases['response_code'])
            print('field_null')
            Assertions.assert_json_value(response, "error", "==", testcases['response_body']['error'])
        elif testcases['type'] == 'password_format_error':
            response = self.user_flow.register_user(username=testcases['request_data']['username'],
                                                    email=testcases['request_data']['email'],
                                                    password=testcases['request_data']['password'])
            Assertions.assert_status_code(response, testcases['response_code'])
            print('password_format_error')
            Assertions.assert_json_value(response, "error", "==", testcases['response_body']['error'])
            Assertions.assert_json_value(response, "details", "==", testcases['response_body']['details'])

    @pytest.fixture(scope="class", autouse=True)
    def clean_db(self):
        yield
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = int(os.getenv("DB_PORT", "5432"))
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD")  # 从环境变量读取密码，如果没有则使用空字符串
        db_name = os.getenv("DB_NAME", "testhub")
        try:
            # 1. 建立连接
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            print("数据库连接成功！")

            # 2. 创建游标
            cur = conn.cursor()

            # 3. 执行操作
            # 使用参数化查询防止SQL注入
            delete_query = "Delete FROM public.\"User\" WHERE username like '%api_auto_user%'"
            cur.execute(delete_query)
            conn.commit()  # 提交事务
            cur.close()
        except Exception as e:
            print(f"数据库操作出错: {e}")
