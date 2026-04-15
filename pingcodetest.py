import os
from pprint import pprint

from dotenv import load_dotenv

from core.pingcode_client import PingCodeClient
from data.data_loader import load_test_data

load_dotenv()

client_id = os.getenv('PINGCODECLINETID')
client_secret = os.getenv('PINGCODECLINETSECRET')
base_url = 'https://open.pingcode.com'

ping_code_client = PingCodeClient(server_url=base_url, client_id=client_id, client_secret=client_secret,
                                  project_name='API_QAForge')
# ping_code_client.create_test_plan_by_library_id('创建测试计划测试', 'huan')
# pprint(ping_code_client.get_testcases_id_by_suite_name('注册登录模块'))
# ping_code_client.create_plan_and_add_testcases('注册登录模块', '注册登录模块自动化', 'huan')
data = load_test_data('register_cases.yaml')
pprint(data)
