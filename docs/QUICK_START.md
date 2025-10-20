# 🚀 ChatBox 后端快速启动指南

## 📋 前置条件
- Python 3.8+
- MySQL 服务运行中
- 虚拟环境已激活

## ⚡ 快速启动步骤

### 1. 激活虚拟环境
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 设置数据库
```bash
python setup_database.py
```

### 4. 运行测试（可选）
```bash
python run_tests.py
```

### 5. 启动服务
```bash
# 方式一：使用修复后的启动脚本
python run_server.py

# 方式二：使用原始启动脚本
python start.py
```

## 🔧 服务地址
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 🧪 测试API
服务启动后，在另一个终端运行：
```bash
python tests/test_api.py
```

## 📊 项目结构
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
│   └── llm_service.py   # LLM服务
├── routers/             # 路由模块
│   ├── users.py         # 用户接口
│   ├── conversations.py # 会话接口
│   └── messages.py      # 消息接口
├── tests/               # 测试文件
├── requirements.txt     # 依赖列表
├── setup_database.py    # 数据库设置
├── run_server.py        # 服务器启动
└── README.md            # 详细文档
```

## 🎯 核心功能
- ✅ 用户注册/登录（JWT认证）
- ✅ 多会话管理
- ✅ 流式消息输出
- ✅ 历史记录查询
- ✅ 会话标题自动生成
- ✅ 联网搜索支持
- ✅ 深度思考模式

## 🐛 常见问题

### 问题1：数据库连接失败
**解决方案**：
1. 确保MySQL服务正在运行
2. 检查config.py中的数据库配置
3. 运行`python setup_database.py`创建数据库

### 问题2：服务启动失败
**解决方案**：
1. 使用`python run_server.py`而不是`python start.py`
2. 检查端口8000是否被占用
3. 确保所有依赖已安装

### 问题3：LLM API调用失败
**解决方案**：
1. 检查config.py中的SiliconFlow API密钥
2. 确保网络连接正常
3. 运行`python tests/test_llm.py`测试LLM服务

## 📝 下一步
后端服务启动成功后，可以开始前端开发或使用API进行测试。
