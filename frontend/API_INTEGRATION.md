# 🚀 前端-后端API集成指南

## 📋 概述

本项目实现了完整的前端-后端API集成，支持所有CRUD操作和流式消息处理。

## 🏗️ 架构设计

### 后端API (FastAPI)
- **用户管理**: 注册、登录、信息更新、账户删除
- **会话管理**: 创建、获取、更新标题、删除会话
- **消息管理**: 发送、获取、更新内容、删除消息
- **流式响应**: 支持实时消息流处理

### 前端服务层 (Vue 3 + Pinia)
- **统一API服务**: `services/api.js` - 封装所有API调用
- **状态管理**: `stores/auth.js` 和 `stores/chat.js` - 管理应用状态
- **错误处理**: 统一的错误处理和用户反馈
- **类型定义**: JSDoc类型注释提供开发时类型检查

## 🔧 使用方法

### 1. 启动服务

```bash
# 启动后端服务
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端服务
cd frontend
npm run dev
```

### 2. 访问测试页面

- **Swagger UI**: http://localhost:8000/docs
- **前端应用**: http://localhost:5173
- **API测试页面**: http://localhost:5173/api-test
- **独立测试页面**: 打开 `frontend_api_test.html`

### 3. API服务使用示例

#### 用户认证
```javascript
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

// 用户注册
const result = await authStore.register('username', 'password')

// 用户登录
const result = await authStore.login('username', 'password')

// 更新用户信息
const result = await authStore.updateUserInfo({
  username: 'newusername',
  password: 'newpassword'
})

// 删除用户账户
const result = await authStore.deleteAccount()
```

#### 会话管理
```javascript
import { useChatStore } from './stores/chat'

const chatStore = useChatStore()

// 创建会话
const conversation = await chatStore.createConversation('会话标题')

// 获取会话列表
await chatStore.fetchConversations()

// 选择会话
await chatStore.selectConversation(conversation)

// 更新会话标题
await chatStore.updateConversationTitle(conversationId, '新标题')

// 删除会话
await chatStore.deleteConversation(conversationId)
```

#### 消息管理
```javascript
// 发送消息（流式）
await chatStore.sendMessage(
  '消息内容',
  false, // enableSearch
  true,  // enableThinking
  (chunk) => {
    // 处理流式数据
    console.log('接收到数据块:', chunk)
  },
  (error) => {
    // 处理错误
    console.error('发送失败:', error)
  },
  () => {
    // 完成回调
    console.log('发送完成')
  }
)

// 获取消息列表
await chatStore.fetchMessages(conversationId)

// 更新消息内容
await chatStore.updateMessageContent(messageId, '新内容')

// 删除消息
await chatStore.deleteMessage(messageId)
```

## 📊 API接口列表

### 用户相关
- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息
- `DELETE /api/users/me` - 删除用户账户

### 会话相关
- `GET /api/conversations/` - 获取会话列表
- `POST /api/conversations/` - 创建会话
- `GET /api/conversations/{id}` - 获取特定会话
- `PUT /api/conversations/{id}` - 更新会话标题
- `DELETE /api/conversations/{id}` - 删除会话

### 消息相关
- `POST /api/messages/send` - 发送消息（流式）
- `GET /api/messages/conversation/{id}` - 获取会话消息
- `PUT /api/messages/{id}` - 更新消息内容
- `DELETE /api/messages/{id}` - 删除消息

## 🔒 认证机制

所有需要认证的API都使用JWT Bearer Token：

```javascript
// 自动添加认证头
headers: {
  'Authorization': `Bearer ${token}`
}
```

## 🚨 错误处理

所有API调用都包含统一的错误处理：

```javascript
try {
  const result = await someApiCall()
  // 处理成功结果
} catch (error) {
  // 错误信息格式
  console.error({
    message: error.message,    // 错误消息
    status: error.status,      // HTTP状态码
    data: error.data          // 服务器返回的错误数据
  })
}
```

## 🧪 测试

### 自动化测试
```bash
# 后端API测试
python test_api.py
python test_new_apis.py

# 快速测试
python quick_test.py
```

### 手动测试
1. 打开 `frontend_api_test.html` 进行独立测试
2. 访问 http://localhost:8000/docs 使用Swagger UI
3. 访问 http://localhost:5173/api-test 使用前端测试页面

## 📝 开发建议

### 1. 添加新API
1. 在后端添加路由和schema
2. 在前端 `services/api.js` 中添加对应方法
3. 在相应的store中添加状态管理
4. 更新类型定义

### 2. 错误处理
- 使用 `handleApiError` 函数统一处理错误
- 在store中提供用户友好的错误消息
- 记录详细的错误日志用于调试

### 3. 状态管理
- 使用Pinia store管理应用状态
- 保持状态与服务器数据同步
- 合理使用computed属性

### 4. 性能优化
- 使用流式API处理大量数据
- 实现适当的缓存策略
- 避免不必要的API调用

## 🔄 数据流

```
用户操作 → Vue组件 → Pinia Store → API服务 → 后端API → 数据库
                ↓
            状态更新 → 组件重新渲染 → 用户界面更新
```

## 🎯 下一步计划

1. **实时通信**: 添加WebSocket支持
2. **离线支持**: 实现离线数据同步
3. **性能监控**: 添加API性能监控
4. **缓存策略**: 实现智能缓存机制
5. **类型安全**: 迁移到TypeScript

## 📞 支持

如有问题，请查看：
1. 后端日志: 控制台输出
2. 前端控制台: 浏览器开发者工具
3. 网络请求: 浏览器网络面板
4. API文档: http://localhost:8000/docs
