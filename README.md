# API QAForge

基于 Python + pytest 的 API 接口自动化测试框架。

## 目录结构

```
API_QAForge/
├── config/
│   ├── settings.py          # 配置加载器
│   └── environments.yaml    # 环境配置
├── core/
│   ├── api_client.py        # HTTP 客户端封装
│   ├── assertions.py        # 响应断言工具
│   ├── auth.py              # 认证管理
│   └── hooks.py             # 请求钩子
├── data/
│   ├── data_loader.py       # 数据加载器
│   └── test_data/           # 测试数据
├── tests/
│   ├── conftest.py          # pytest fixtures
│   └── test_example.py      # 示例测试
├── reports/                 # 测试报告
├── utils/
│   ├── logger.py            # 日志工具
│   └── helpers.py           # 辅助函数
└── pytest.ini
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

在 `config/environments.yaml` 中配置不同环境的 API 地址：

```yaml
environments:
  dev:
    base_url: "http://localhost:8080"
    timeout: 30
  staging:
    base_url: "https://staging-api.example.com"
  prod:
    base_url: "https://api.example.com"
default: dev
```

通过环境变量切换：`ENV=staging pytest`

## 使用方法

### 运行所有测试

```bash
pytest
```

### 运行特定标记的测试

```bash
pytest -m smoke      # 只运行冒烟测试
pytest -m regression # 只运行回归测试
```

### 生成 Allure 报告

```bash
# 生成报告
allure serve reports/allure-results

# 或生成静态文件
allure generate reports/allure-results -o reports/allure-report
```

### 并行执行

```bash
pytest -n auto
```

## 示例测试

```python
from core.assertions import Assertions
from core.api_client import APIClient

client = APIClient(base_url="http://localhost:8080")
assertions = Assertions()

# GET 请求
response = client.get("/users/1")
assertions.assert_status_code(response, 200)
assertions.assert_json_path(response, "id", 1)

# POST 请求
payload = {"name": "Test", "email": "test@example.com"}
response = client.post("/users", json=payload)
assertions.assert_status_code(response, 201)
```

## 数据驱动测试

```python
import pytest
from data.data_loader import load_test_data

@pytest.mark.parametrize("user", load_test_data("users.yaml"))
def test_user_creation(api_client, user):
    response = api_client.post("/users", json=user)
    assertions.assert_status_code(response, 201)
```

## 认证

```python
from core.auth import AuthManager

auth = AuthManager(api_client)
auth.login(username="admin", password="secret")
# 后续请求自动携带 Bearer Token
response = api_client.get("/protected-resource")
```

## 断言工具

```python
assertions.assert_status_code(response, 200)
assertions.assert_json_path(response, "data.name", "John")
assertions.assert_response_time(response, 1000)  # 1000ms
assertions.assert_header_exists(response, "Content-Type")
assertions.assert_json_value(response, "count", ">", 0)
```
