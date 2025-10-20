# ChatBox 后端服务

## 项目简介
ChatBox 是一个轻量级的仿 ChatGPT 聊天应用的后端服务，基于 FastAPI + MySQL 构建。

## 功能特性
- ✅ 用户注册/登录（JWT认证）
- ✅ 多会话管理
- ✅ 流式消息输出
- ✅ 历史记录查询
- ✅ 会话标题自动生成
- ✅ 联网搜索支持
- ✅ 深度思考模式

## 技术栈
- **框架**: FastAPI
- **数据库**: MySQL + SQLAlchemy
- **认证**: JWT
- **LLM**: SiliconFlow API
- **流式输出**: Server-Sent Events

## 快速开始

### 方式一：本地开发

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 配置数据库
确保 MySQL 服务正在运行，并创建数据库：
```sql
CREATE DATABASE chatbox CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3. 初始化数据库
```bash
python init_db.py
```

#### 4. 运行测试（可选）
```bash
python run_tests.py
```

#### 5. 启动服务
```bash
python start.py
```

服务将在 http://localhost:8000 启动

### 方式二：Docker部署

#### 1. 使用Docker Compose
```bash
docker-compose up -d
```

#### 2. 查看日志
```bash
docker-compose logs -f backend
```

#### 3. 停止服务
```bash
docker-compose down
```

## API 文档
启动服务后，访问 http://localhost:8000/docs 查看完整的 API 文档。

## 主要接口

### 用户管理
- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息

### 会话管理
- `GET /api/conversations/` - 获取会话列表
- `POST /api/conversations/` - 创建新会话
- `GET /api/conversations/{id}` - 获取会话详情
- `DELETE /api/conversations/{id}` - 删除会话

### 消息管理
- `GET /api/messages/conversation/{id}` - 获取会话消息
- `POST /api/messages/send` - 发送消息（流式）
- `DELETE /api/messages/{id}` - 删除消息

## 测试说明

### 运行测试
```bash
# 运行所有测试
python run_tests.py

# 或分别运行
python tests/test_database.py    # 数据库测试
python tests/test_llm.py         # LLM服务测试
python tests/test_api.py         # API接口测试
```

### 测试内容
- **数据库测试**: 连接、表创建、CRUD操作
- **LLM服务测试**: API调用、流式输出、标题生成
- **API接口测试**: 用户注册/登录、会话管理、消息发送

## 配置说明
在 `config.py` 中可以修改以下配置：
- 数据库连接信息
- JWT 密钥和过期时间
- SiliconFlow API 配置

## 数据库结构
- `users` - 用户表
- `conversations` - 会话表
- `messages` - 消息表

详细结构请参考 `models.py` 文件。

## 项目结构
```
backend/
├── main.py              # FastAPI应用入口
├── config.py            # 配置文件
├── database.py          # 数据库连接
├── models.py            # 数据模型
├── schemas.py           # Pydantic模型
├── auth.py              # 认证模块
├── utils.py             # 工具函数
├── services/            # 服务层
│   ├── llm_service.py   # LLM服务
│   └── __init__.py
├── routers/             # 路由模块
│   ├── users.py         # 用户接口
│   ├── conversations.py # 会话接口
│   ├── messages.py      # 消息接口
│   └── __init__.py
├── tests/               # 测试文件
│   ├── test_database.py # 数据库测试
│   ├── test_llm.py      # LLM测试
│   ├── test_api.py      # API测试
│   └── run_all_tests.py # 测试运行器
├── requirements.txt     # 依赖列表
├── Dockerfile          # Docker配置
├── docker-compose.yml  # Docker Compose配置
└── README.md           # 说明文档
```

## 故障排除

### 常见问题
1. **数据库连接失败**: 检查MySQL服务是否启动，用户名密码是否正确
2. **LLM API调用失败**: 检查SiliconFlow API密钥是否有效
3. **端口占用**: 修改`start.py`中的端口号
4. **依赖安装失败**: 确保Python版本>=3.8，使用虚拟环境

### 日志查看
```bash
# 查看应用日志
python start.py

# Docker环境查看日志
docker-compose logs -f backend
```
