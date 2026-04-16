import time
from datetime import datetime, timedelta
import requests


class PingCodeClient:
    def __init__(self, server_url, client_id, client_secret, project_name):
        self.server_url = server_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_name = project_name
        self.headers = {
            "Authorization": f"Bearer {self.get_token()}"
        }

    def get_token(self):
        """
        获取token
        :return: token
        """
        get_token_url = f"{self.server_url}/v1/auth/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.get(url=get_token_url, params=params)
        return response.json()['access_token']

    def get_libraries_id(self):
        """
        获取库ID
        :return: 库ID
        """
        get_libraries_url = f"{self.server_url}/v1/testhub/libraries"
        response = requests.get(url=get_libraries_url, headers=self.headers)
        for lib in response.json()['values']:
            if lib['name'] == self.project_name:
                return lib['id']
        return None

    def get_person_id(self, display_name):
        """
        获取人员ID
        :param display_name: 人员名称
        :return: 人员ID
        """
        get_person_url = f"{self.server_url}/v1/directory/users"
        response = requests.get(url=get_person_url, headers=self.headers)
        for person in response.json()['values']:
            if person['display_name'] == display_name:
                return person['id']
        return None

    def create_test_plan_by_library_id(self, plan_name, assignee_name):
        """
        创建测试计划
        :param plan_name: 测试计划名称
        :param assignee_name: 测试计划负责人名称
        :return: 测试计划ID
        """
        create_test_plan_url = f"{self.server_url}/v1/testhub/libraries/{self.get_libraries_id()}/plans"
        now_timestamp = int(time.time())
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_timestamp = int(tomorrow.timestamp())
        plan_name = f"{plan_name}_{now_timestamp}"
        payload = {
            "name": plan_name,
            "type_id": "69dc9a70d21bc6b5a599fa77",  # 普通的类型
            "start_at": now_timestamp,
            "end_at": tomorrow_timestamp,
            "assignee_id": self.get_person_id(assignee_name)
        }
        response = requests.post(url=create_test_plan_url, json=payload, headers=self.headers)
        return response.json()['id']

    def get_testcases_id_by_suite_name(self, suite_name):
        """

        """
        get_testcases_url = f"{self.server_url}/v1/testhub/cases"
        params = {
            "library_id": self.get_libraries_id()
        }
        response = requests.get(url=get_testcases_url, params=params, headers=self.headers)
        testcase_id_list = []
        for value in response.json()['values']:
            if value['suite']['name'] == suite_name:
                testcase_id_list.append(value['id'])
        return testcase_id_list

    def delete_test_plan_by_id(self, plan_id):
        """
        删除测试计划
        """
        delete_test_plan_url = f"{self.server_url}/v1/testhub/plans/{plan_id}"
        response = requests.delete(url=delete_test_plan_url, headers=self.headers)
        return response.json()

    def create_plan_and_add_testcases(self, suite_name, plan_name, assignee_name):
        """
        根据用例模块创建测试计划并添加测试用例
        :return: 测试用例名字和执行用例id
        """
        add_testcases_to_plan_url = f"{self.server_url}/v1/testhub/runs/bulk"
        testcases_id = self.get_testcases_id_by_suite_name(suite_name)
        plan_id = self.create_test_plan_by_library_id(plan_name=plan_name, assignee_name=assignee_name)
        library_id = self.get_libraries_id()
        payload = {"runs": []}
        if len(testcases_id) <= 100:
            for testcase_id in testcases_id:
                testcase_payload = {
                    "library_id": library_id,
                    "plan_id": plan_id,
                    "case_id": testcase_id
                }
                payload["runs"].append(testcase_payload)
        else:
            raise Exception("测试用例数量超过100，请分批添加")
        response = requests.post(url=add_testcases_to_plan_url, json=payload, headers=self.headers)
        # result_list = []
        # for result in response.json():
        #     result_list.append(result['state'])
        # if 'failure' in result_list:
        #     raise Exception("有测试用例添加失败")
        # else:
        #     return True
        testcases_dict = {}
        # 如果有用例添加失败？ 删除测试计划并重新添加？
        for run in response.json():
            if run['state'] == 'failure':
                return None
            else:
                testcases_dict[run['run']['case']['title']] = run['run']['id']
        return testcases_dict

    def execute_testcase(self, run_id, status):
        update_run_url = f"{self.server_url}/v1/testhub/runs/{run_id}"
        status_id = '697b107907a26f9508d52036' if status == 'passed' else '697b107907a26f9508d52037'
        payload = {
            "status_id": status_id
        }
        response = requests.patch(url=update_run_url, json=payload, headers=self.headers)
        return response

