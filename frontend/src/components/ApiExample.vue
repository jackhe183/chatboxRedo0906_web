<template>
  <div class="api-example">
    <h2>🔧 API使用示例</h2>
    
    <!-- 用户管理示例 -->
    <div class="example-section">
      <h3>👤 用户管理</h3>
      <div class="form-group">
        <input v-model="userForm.username" placeholder="用户名" />
        <input v-model="userForm.password" type="password" placeholder="密码" />
        <button @click="registerUser" :disabled="loading">注册</button>
        <button @click="loginUser" :disabled="loading">登录</button>
        <button @click="updateUser" :disabled="loading || !isLoggedIn">更新用户</button>
        <button @click="deleteUser" :disabled="loading || !isLoggedIn">删除用户</button>
      </div>
      <div v-if="user" class="user-info">
        <p>当前用户: {{ user.username }} (ID: {{ user.id }})</p>
      </div>
    </div>

    <!-- 会话管理示例 -->
    <div class="example-section">
      <h3>💬 会话管理</h3>
      <div class="form-group">
        <input v-model="conversationForm.title" placeholder="会话标题" />
        <button @click="createConversation" :disabled="loading || !isLoggedIn">创建会话</button>
        <button @click="fetchConversations" :disabled="loading || !isLoggedIn">获取会话列表</button>
      </div>
      <div v-if="conversations.length > 0" class="conversation-list">
        <h4>会话列表:</h4>
        <div v-for="conv in conversations" :key="conv.id" class="conversation-item">
          <span>{{ conv.title }} ({{ conv.message_count }} 条消息)</span>
          <button @click="selectConversation(conv)" :disabled="loading">选择</button>
          <button @click="updateConversationTitle(conv)" :disabled="loading">更新标题</button>
          <button @click="deleteConversation(conv.id)" :disabled="loading">删除</button>
        </div>
      </div>
    </div>

    <!-- 消息管理示例 -->
    <div class="example-section">
      <h3>📝 消息管理</h3>
      <div v-if="currentConversation" class="current-conversation">
        <p>当前会话: {{ currentConversation.title }}</p>
        <div class="form-group">
          <input v-model="messageForm.content" placeholder="消息内容" />
          <button @click="sendMessage" :disabled="loading || !isLoggedIn">发送消息</button>
          <button @click="fetchMessages" :disabled="loading || !isLoggedIn">获取消息</button>
        </div>
        <div v-if="messages.length > 0" class="message-list">
          <h4>消息列表:</h4>
          <div v-for="msg in messages" :key="msg.id" class="message-item">
            <span class="message-role">{{ msg.role }}:</span>
            <span class="message-content">{{ msg.content }}</span>
            <button @click="updateMessage(msg)" :disabled="loading || msg.role !== 'user'">编辑</button>
            <button @click="deleteMessage(msg.id)" :disabled="loading">删除</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>请先选择一个会话</p>
      </div>
    </div>

    <!-- 日志显示 -->
    <div class="log-section">
      <h3>📋 操作日志</h3>
      <div class="log-container">
        <div v-for="(log, index) in logs" :key="index" :class="['log-item', log.type]">
          [{{ log.time }}] {{ log.message }}
        </div>
      </div>
      <button @click="clearLogs">清除日志</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'

const authStore = useAuthStore()
const chatStore = useChatStore()

// 响应式数据
const userForm = ref({
  username: 'testuser',
  password: 'testpass'
})

const conversationForm = ref({
  title: '测试会话'
})

const messageForm = ref({
  content: '你好，这是一条测试消息'
})

const logs = ref([])

// 计算属性
const isLoggedIn = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const conversations = computed(() => chatStore.conversations)
const currentConversation = computed(() => chatStore.currentConversation)
const messages = computed(() => chatStore.currentMessages)
const loading = computed(() => authStore.loading || chatStore.loading)

// 日志函数
const addLog = (message, type = 'info') => {
  logs.value.unshift({
    time: new Date().toLocaleTimeString(),
    message,
    type
  })
  // 限制日志数量
  if (logs.value.length > 50) {
    logs.value = logs.value.slice(0, 50)
  }
}

const clearLogs = () => {
  logs.value = []
}

// 用户管理方法
const registerUser = async () => {
  try {
    addLog('开始用户注册...', 'info')
    const result = await authStore.register(userForm.value.username, userForm.value.password)
    if (result.success) {
      addLog('用户注册成功', 'success')
    } else {
      addLog(`用户注册失败: ${result.error}`, 'error')
    }
  } catch (error) {
    addLog(`用户注册异常: ${error.message}`, 'error')
  }
}

const loginUser = async () => {
  try {
    addLog('开始用户登录...', 'info')
    const result = await authStore.login(userForm.value.username, userForm.value.password)
    if (result.success) {
      addLog('用户登录成功', 'success')
    } else {
      addLog(`用户登录失败: ${result.error}`, 'error')
    }
  } catch (error) {
    addLog(`用户登录异常: ${error.message}`, 'error')
  }
}

const updateUser = async () => {
  try {
    addLog('开始更新用户信息...', 'info')
    const result = await authStore.updateUserInfo({
      username: 'updateduser',
      password: 'newpassword'
    })
    if (result.success) {
      addLog('用户信息更新成功', 'success')
    } else {
      addLog(`用户信息更新失败: ${result.error}`, 'error')
    }
  } catch (error) {
    addLog(`用户信息更新异常: ${error.message}`, 'error')
  }
}

const deleteUser = async () => {
  try {
    addLog('开始删除用户账户...', 'info')
    const result = await authStore.deleteAccount()
    if (result.success) {
      addLog('用户账户删除成功', 'success')
    } else {
      addLog(`用户账户删除失败: ${result.error}`, 'error')
    }
  } catch (error) {
    addLog(`用户账户删除异常: ${error.message}`, 'error')
  }
}

// 会话管理方法
const createConversation = async () => {
  try {
    addLog('开始创建会话...', 'info')
    const conversation = await chatStore.createConversation(conversationForm.value.title)
    addLog(`会话创建成功: ${conversation.title} (ID: ${conversation.id})`, 'success')
  } catch (error) {
    addLog(`会话创建失败: ${error.message}`, 'error')
  }
}

const fetchConversations = async () => {
  try {
    addLog('开始获取会话列表...', 'info')
    await chatStore.fetchConversations()
    addLog(`获取会话列表成功，共 ${conversations.value.length} 个会话`, 'success')
  } catch (error) {
    addLog(`获取会话列表失败: ${error.message}`, 'error')
  }
}

const selectConversation = async (conversation) => {
  try {
    addLog(`开始选择会话: ${conversation.title}`, 'info')
    await chatStore.selectConversation(conversation)
    addLog(`会话选择成功: ${conversation.title}`, 'success')
  } catch (error) {
    addLog(`会话选择失败: ${error.message}`, 'error')
  }
}

const updateConversationTitle = async (conversation) => {
  try {
    const newTitle = prompt('请输入新的会话标题:', conversation.title)
    if (newTitle && newTitle !== conversation.title) {
      addLog(`开始更新会话标题: ${conversation.title} -> ${newTitle}`, 'info')
      await chatStore.updateConversationTitle(conversation.id, newTitle)
      addLog(`会话标题更新成功: ${newTitle}`, 'success')
    }
  } catch (error) {
    addLog(`会话标题更新失败: ${error.message}`, 'error')
  }
}

const deleteConversation = async (conversationId) => {
  try {
    addLog(`开始删除会话: ${conversationId}`, 'info')
    await chatStore.deleteConversation(conversationId)
    addLog(`会话删除成功: ${conversationId}`, 'success')
  } catch (error) {
    addLog(`会话删除失败: ${error.message}`, 'error')
  }
}

// 消息管理方法
const sendMessage = async () => {
  try {
    addLog('开始发送消息...', 'info')
    await chatStore.sendMessage(
      messageForm.value.content,
      false, // enableSearch
      true,  // enableThinking
      (chunk) => {
        addLog(`接收到数据块: ${chunk.type}`, 'info')
      },
      (error) => {
        addLog(`消息发送错误: ${error.message}`, 'error')
      },
      () => {
        addLog('消息发送完成', 'success')
      }
    )
  } catch (error) {
    addLog(`消息发送失败: ${error.message}`, 'error')
  }
}

const fetchMessages = async () => {
  try {
    addLog('开始获取消息列表...', 'info')
    await chatStore.fetchMessages(currentConversation.value.id)
    addLog(`获取消息列表成功，共 ${messages.value.length} 条消息`, 'success')
  } catch (error) {
    addLog(`获取消息列表失败: ${error.message}`, 'error')
  }
}

const updateMessage = async (message) => {
  try {
    const newContent = prompt('请输入新的消息内容:', message.content)
    if (newContent && newContent !== message.content) {
      addLog(`开始更新消息内容: ${message.id}`, 'info')
      await chatStore.updateMessageContent(message.id, newContent)
      addLog(`消息内容更新成功: ${message.id}`, 'success')
    }
  } catch (error) {
    addLog(`消息内容更新失败: ${error.message}`, 'error')
  }
}

const deleteMessage = async (messageId) => {
  try {
    addLog(`开始删除消息: ${messageId}`, 'info')
    await chatStore.deleteMessage(messageId)
    addLog(`消息删除成功: ${messageId}`, 'success')
  } catch (error) {
    addLog(`消息删除失败: ${error.message}`, 'error')
  }
}

// 组件挂载时获取用户信息
onMounted(async () => {
  if (isLoggedIn.value) {
    addLog('检测到已登录用户，获取用户信息...', 'info')
    await authStore.fetchUserInfo()
    addLog('用户信息获取完成', 'success')
  }
})
</script>

<style scoped>
.api-example {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.example-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #f9f9f9;
}

.example-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #4a72ff;
  padding-bottom: 10px;
}

.form-group {
  margin: 15px 0;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.form-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group button {
  padding: 8px 16px;
  background: #4a72ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.form-group button:hover:not(:disabled) {
  background: #3d5fe0;
}

.form-group button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.user-info {
  margin: 10px 0;
  padding: 10px;
  background: #e7f3ff;
  border-radius: 4px;
  border-left: 4px solid #4a72ff;
}

.conversation-list, .message-list {
  margin: 15px 0;
}

.conversation-item, .message-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  margin: 5px 0;
  background: white;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

.conversation-item button, .message-item button {
  padding: 4px 8px;
  font-size: 12px;
  background: #6c757d;
}

.conversation-item button:hover, .message-item button:hover {
  background: #5a6268;
}

.message-role {
  font-weight: bold;
  color: #4a72ff;
  min-width: 60px;
}

.message-content {
  flex: 1;
  word-break: break-word;
}

.current-conversation {
  margin: 15px 0;
  padding: 15px;
  background: #e7f3ff;
  border-radius: 4px;
  border-left: 4px solid #4a72ff;
}

.log-section {
  margin-top: 30px;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 10px;
  background: #f8f9fa;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-item {
  margin: 2px 0;
  padding: 2px 0;
}

.log-item.success {
  color: #28a745;
}

.log-item.error {
  color: #dc3545;
}

.log-item.info {
  color: #333;
}
</style>
