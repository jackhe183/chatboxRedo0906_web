# DeepSeek ChatBox

一个轻量级的仿ChatGPT聊天应用，支持深度思考和联网搜索功能。

## 🚀 快速开始

### 1. 启动后端服务

**Windows:**
```bash
# 双击运行
start_backend.bat

# 或命令行运行
cd backend
python app.py
```

**Linux/Mac:**
```bash
# 运行脚本
./start_backend.sh

# 或命令行运行
cd backend
python app.py
```

后端服务将在 `http://localhost:8000` 启动

### 2. 打开前端页面

在浏览器中打开 `frontend/静态对话页面.html` 文件

## ✨ 功能特性

### 🔐 用户系统
- 用户注册/登录
- JWT Token 认证
- 自动登录状态保持

### 💬 聊天功能
- 实时消息发送/接收
- 流式AI响应（打字机效果）
- 深度思考模式 🧠
- 联网搜索模式 🌐
- Markdown 渲染支持

### 📚 会话管理
- 创建新对话
- 历史对话列表
- 按时间分组显示（今天/7天内/30天内）
- 会话标题自动生成

### 🎨 用户界面
- 响应式设计
- 侧边栏收起/展开
- 现代化UI设计
- 流畅的动画效果

## 🛠️ 技术架构

### 后端 (FastAPI)
- **框架**: FastAPI + SQLAlchemy
- **数据库**: SQLite
- **认证**: JWT Token
- **AI服务**: DeepSeek API
- **流式响应**: Server-Sent Events

### 前端 (Vue 3)
- **框架**: Vue 3 Composition API
- **样式**: 原生CSS + CSS变量
- **HTTP客户端**: Fetch API
- **流式处理**: Server-Sent Events
- **Markdown渲染**: marked.js

## 📁 项目结构

```
├── backend/                 # 后端代码
│   ├── app.py              # FastAPI应用入口
│   ├── routers/            # API路由
│   ├── services/           # 业务逻辑服务
│   ├── database/           # 数据库相关
│   └── schemas.py          # 数据模型
├── frontend/               # 前端代码
│   ├── 静态对话页面.html    # 主页面
│   └── README.md           # 前端说明
├── docs/                   # 文档
│   └── 总架构.md           # 架构设计文档
├── start_backend.bat       # Windows启动脚本
├── start_backend.sh        # Linux/Mac启动脚本
└── README.md               # 项目说明
```

## 🔧 开发说明

### 后端API接口

- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息
- `GET /api/conversations/` - 获取会话列表
- `POST /api/conversations/` - 创建新会话
- `GET /api/messages/conversation/{id}` - 获取会话消息
- `POST /api/messages/send` - 发送消息（流式响应）

### 前端特性

- 完全响应式设计
- 实时流式消息接收
- 自动Token管理
- 错误处理和用户反馈
- 本地状态持久化

## 🔒 安全特性

- JWT Token 认证
- 自动Token验证和刷新
- 用户数据隔离
- 输入验证和错误处理

## 📝 使用说明

1. **首次使用**: 注册新账号
2. **开始聊天**: 在输入框输入消息
3. **功能开关**: 开启深度思考或联网搜索
4. **历史对话**: 左侧边栏管理历史对话
5. **新建对话**: 点击"+ 开启新对话"

## 🚨 注意事项

- 确保后端服务运行在 `http://localhost:8000`
- 首次使用需要注册账号
- 支持流式响应，AI回复会逐字显示
- 所有数据都会保存到后端数据库
- 需要配置DeepSeek API密钥（在backend/config.py中）

## 📄 许可证

MIT License
