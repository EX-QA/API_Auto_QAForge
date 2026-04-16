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
# run_json = ping_code_client.create_plan_and_add_testcases('注册登录模块', '注册登录模块自动化', 'huan')
# data = load_test_data('register_cases.yaml')
# pprint(run_json)
run_dic = {'/auth/register - POST - 密码为空': '69e06dd77126d10332f9e99f',
           '/auth/register - POST - 密码无大写字母': '69e06dd7d5bc0f27288aa61e',
           '/auth/register - POST - 密码无小写字母': '69e06dd78bdd46f5b46cc59f',
           '/auth/register - POST - 密码无数字': '69e06dd76cc9f5d6d7761306',
           '/auth/register - POST - 密码无特殊字符': '69e06dd77126d10332f9e9a1',
           '/auth/register - POST - 密码是纯字母': '69e06dd78bdd46f5b46cc5a0',
           '/auth/register - POST - 密码是纯数字': '69e06dd7d5bc0f27288aa621',
           '/auth/register - POST - 密码正好8字符': '69e06dd7d5bc0f27288aa620',
           '/auth/register - POST - 密码长度不足8位': '69e06dd76cc9f5d6d7761304',
           '/auth/register - POST - 成功注册新用户': '69e06dd7d5bc0f27288aa61c',
           '/auth/register - POST - 所有字段为空': '69e06dd77126d10332f9e9a2',
           '/auth/register - POST - 用户名为空': '69e06dd76cc9f5d6d7761302',
           '/auth/register - POST - 用户名已存在': '69e06dd77126d10332f9e9a5',
           '/auth/register - POST - 用户名超长（100字符）': '69e06dd78bdd46f5b46cc59e',
           '/auth/register - POST - 邮箱为空': '69e06dd78bdd46f5b46cc59c',
           '/auth/register - POST - 邮箱已存在': '69e06dd76cc9f5d6d7761308'}
result = ping_code_client.execute_testcase('69e06dd76cc9f5d6d7761308', 'failed')
print(result.status_code)
