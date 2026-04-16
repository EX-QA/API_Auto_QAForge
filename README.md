# API_QAForge

基于 Python + pytest 的 API 接口自动化测试框架，支持多环境配置、数据驱动测试、Allure 报告以及 PingCode 测试管理平台集成。

## 功能特性

- **HTTP 客户端封装** - 支持 GET/POST/PUT/PATCH/DELETE 方法，自动管理 URL 构建、请求头、超时和 SSL 验证
- **丰富断言工具** - 支持状态码、JSON 路径、响应时间、Header、灵活比较等多种断言
- **认证管理** - 支持 Bearer Token 和 API Key 两种认证方式
- **数据驱动** - 支持 YAML/JSON/CSV 格式的测试数据
- **多环境配置** - 通过 `environments.yaml` 和环境变量切换不同测试环境
- **测试报告** - 集成 Allure 报告，支持可视化测试结果
- **并行执行** - 支持 pytest-xdist 分布式并行执行
- **失败重试** - 内置测试失败重试机制，提高测试稳定性
- **请求钩子** - 支持注册请求前/后的钩子函数，用于日志记录、性能追踪等
- **PingCode 集成** - 自动同步测试结果到 PingCode 测试管理平台

## 目录结构

```
API_QAForge/
├── config/
│   ├── __init__.py
│   ├── settings.py          # 配置加载器（单例模式）
│   └── environments.yaml    # 环境配置
├── core/
│   ├── __init__.py
│   ├── api_client.py        # HTTP 客户端封装
│   ├── assertions.py        # 响应断言工具
│   ├── auth.py              # 认证管理
│   └── hooks.py             # 请求钩子
├── data/
│   ├── __init__.py
│   ├── data_loader.py       # 数据加载器（支持 YAML/JSON/CSV）
│   └── test_data/           # 测试数据目录
│       └── users.yaml
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures 和钩子
│   └── test_register_and_login.py  # 示例测试
├── business/                 # 业务层（封装测试流程）
├── utils/
│   ├── __init__.py
│   ├── logger.py            # 日志工具
│   └── helpers.py           # 辅助函数（数据生成）
├── reports/                  # 测试报告目录
│   └── .gitkeep
├── requirements.txt
└── pytest.ini
```

## 环境配置

### 依赖安装

```bash
pip install -r requirements.txt
```

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ENV` | 运行环境 | `dev` / `staging` / `prod` |
| `PINGCODECLINETID` | PingCode 客户端 ID | - |
| `PINGCODECLINETSECRET` | PingCode 客户端密钥 | - |
| `DB_HOST` | 数据库地址 | `localhost` |
| `DB_PORT` | 数据库端口 | `5432` |
| `DB_USER` | 数据库用户名 | `postgres` |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_NAME` | 数据库名称 | `testhub` |

### 环境配置文件

在 `config/environments.yaml` 中配置不同环境的 API 地址：

```yaml
environments:
  dev:
    base_url: "http://localhost:5173/api/v1"
    timeout: 30
    verify_ssl: false
    pingcode_base_url: "https://open.pingcode.com"
    pingcode_project_name: "API_QAForge"
  staging:
    base_url: "https://staging-api.example.com"
    timeout: 30
    verify_ssl: true
  prod:
    base_url: "https://api.example.com"
    timeout: 60
    verify_ssl: true

default: dev
```

## 运行测试

### 基本命令

```bash
# 运行所有测试
pytest

# 运行特定标记的测试
pytest -m smoke      # 只运行冒烟测试
pytest -m regression # 只运行回归测试
pytest -m critical   # 只运行关键路径测试
```

### 报告生成

```bash
# 生成 Allure 报告
allure serve reports/allure-results

# 或生成静态 HTML 文件
allure generate reports/allure-results -o reports/allure-report
```

### 并行执行

```bash
# 自动检测 CPU 核心数并行执行
pytest -n auto
```

### 指定环境

```bash
ENV=staging pytest
```

## 核心模块

### APIClient

HTTP 客户端封装类，提供简洁的 API 调用接口：

```python
from core.api_client import APIClient

client = APIClient(
    base_url="http://localhost:5173/api/v1",
    timeout=30,
    verify_ssl=False
)

# GET 请求
response = client.get("/users/1")

# POST 请求
response = client.post("/users", json={"name": "test", "email": "test@example.com"})

# PUT 请求
response = client.put("/users/1", json={"name": "updated"})

# PATCH 请求
response = client.patch("/users/1", json={"name": "patched"})

# DELETE 请求
response = client.delete("/users/1")

# 手动设置 Header
client.set_header("Authorization", "Bearer token_value")
client.remove_header("Authorization")

# 关闭会话
client.close()
```

### Assertions

断言工具类，支持多种验证方式：

```python
from core.assertions import Assertions

# 验证状态码
Assertions.assert_status_code(response, 200)

# 验证 JSON 路径和值
Assertions.assert_json_path(response, "data.id", 1)
Assertions.assert_json_value(response, "count", ">", 0)

# 验证响应时间（毫秒）
Assertions.assert_response_time(response, 1000)

# 验证 Header 存在
Assertions.assert_header_exists(response, "Content-Type")

# 验证响应包含文本
Assertions.assert_response_contains(response, "success")
```

### AuthManager

认证管理器，支持 Bearer Token 和 API Key：

```python
from core.auth import AuthManager

auth = AuthManager(api_client)

# 登录并自动设置 Bearer Token
auth.login(username="admin", password="secret")

# 手动设置 Bearer Token
auth.set_bearer_token("your_token_here")

# 或使用 API Key
auth.set_api_key("your_api_key", header_name="X-API-Key")

# 登出
auth.logout()
```

### HooksManager

请求钩子管理器，支持在请求前后执行自定义逻辑：

```python
from core.hooks import HooksManager, LoggingHook, timing_hook

hooks = HooksManager()

# 注册请求日志钩子
hooks.register_pre_request(LoggingHook.log_request)
hooks.register_post_request(LoggingHook.log_response)

# 注册响应时间追踪钩子
hooks.register_post_request(timing_hook)
```

### 数据加载器

支持加载 YAML、JSON、CSV 格式的测试数据：

```python
from data.data_loader import load_test_data

# 加载 YAML 数据
users = load_test_data("users.yaml")

# 指定自定义目录
data = load_test_data("register_cases.yaml", data_dir="/path/to/data")
```

### 辅助工具

```python
from utils.helpers import (
    generate_random_string,  # 生成随机字符串
    generate_random_email,   # 生成随机邮箱
    generate_random_phone,   # 生成随机手机号
    timestamp_now,           # 当前时间戳
    date_offset,             # 日期偏移
    random_choice,          # 随机选择
    build_query_params       # 构建查询参数
)
```

## 测试标记

在 `pytest.ini` 中定义了以下测试标记：

| 标记 | 说明 |
|------|------|
| `smoke` | 冒烟测试 |
| `regression` | 回归测试 |
| `critical` | 关键路径测试 |

## pytest 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --alluredir=reports/allure-results
    --reruns=2
    --reruns-delay=1
    --capture=tee-sys
```

## 最佳实践

1. **使用数据驱动** - 将测试数据与测试逻辑分离，使用 YAML/JSON/CSV 文件管理测试数据
2. **利用 Fixtures** - 使用 pytest fixtures 管理测试依赖，如 API 客户端、认证状态等
3. **业务封装** - 在 `business/` 目录下封装常用测试流程，减少测试代码重复
4. **日志记录** - 使用框架提供的日志工具记录测试过程，便于问题排查
5. **失败重试** - 利用 `--reruns` 配置处理不稳定的测试
6. **环境隔离** - 使用环境变量切换不同测试环境，确保测试环境与生产环境分离
