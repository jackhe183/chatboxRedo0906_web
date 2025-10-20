<template>
  <div class="chat-interface">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>ChatBox</h2>
        <button @click="createNewChat" class="new-chat-btn">
          + 新对话
        </button>
      </div>
      
      <div class="conversations-list">
        <div 
          v-for="conversation in conversations" 
          :key="conversation.id"
          :class="{ active: currentConversation?.id === conversation.id }"
          class="conversation-item"
          @click="selectConversation(conversation)"
        >
          <div class="conversation-title">{{ conversation.title }}</div>
          <div class="conversation-time">{{ formatTime(conversation.updated_at) }}</div>
        </div>
      </div>
      
      <div class="sidebar-footer">
        <div class="user-info">
          <span>{{ user?.username }}</span>
          <button @click="logout" class="logout-btn">退出</button>
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="chat-main">
      <div v-if="!currentConversation" class="welcome-screen">
        <h1>欢迎使用 ChatBox</h1>
        <p>开始一个新的对话吧！</p>
      </div>
      
      <div v-else class="chat-container">
        <!-- 消息列表 -->
        <div class="messages-container" ref="messagesContainer">
          <div 
            v-for="message in currentMessages" 
            :key="message.id"
            :class="['message', message.role]"
          >
            <div class="message-content">
              <div v-if="message.role === 'assistant'" class="message-text" v-html="renderMarkdown(message.content)"></div>
              <div v-else class="message-text">{{ message.content }}</div>
            </div>
            <div class="message-time">{{ formatTime(message.created_at) }}</div>
          </div>
          
          <!-- 流式消息显示 -->
          <div v-if="streamingMessage" class="message assistant">
            <div class="message-content">
              <div class="message-text" v-html="renderMarkdown(streamingMessage)"></div>
              <div class="typing-indicator">正在输入...</div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <div class="input-options">
            <label>
              <input v-model="enableSearch" type="checkbox" />
              联网搜索
            </label>
            <label>
              <input v-model="enableThinking" type="checkbox" />
              深度思考
            </label>
          </div>
          
          <div class="input-container">
            <textarea
              v-model="inputMessage"
              @keydown="handleKeyDown"
              placeholder="输入消息..."
              rows="1"
              ref="messageInput"
            ></textarea>
            <button 
              @click="sendMessage" 
              :disabled="!inputMessage.trim() || sending"
              class="send-btn"
            >
              {{ sending ? '发送中...' : '发送' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { renderMarkdown } from '../utils/markdown'

const router = useRouter()
const authStore = useAuthStore()
const chatStore = useChatStore()

const { user } = authStore
const { 
  conversations, 
  currentConversation, 
  currentMessages, 
  loading 
} = chatStore

const inputMessage = ref('')
const enableSearch = ref(false)
const enableThinking = ref(false)
const sending = ref(false)
const streamingMessage = ref('')
const messagesContainer = ref(null)
const messageInput = ref(null)

onMounted(async () => {
  await chatStore.fetchConversations()
})

const createNewChat = async () => {
  try {
    const newConversation = await chatStore.createConversation()
    await chatStore.selectConversation(newConversation)
  } catch (error) {
    console.error('创建新对话失败:', error)
  }
}

const selectConversation = async (conversation) => {
  await chatStore.selectConversation(conversation)
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || sending.value) return

  const message = inputMessage.value.trim()
  inputMessage.value = ''
  sending.value = true
  streamingMessage.value = ''

  try {
    // 这里需要实现流式接收
    await chatStore.sendMessage(message, enableSearch.value, enableThinking.value)
    
    // 模拟流式接收（实际应该从API流式接收）
    // 这里需要根据后端API的实际实现来调整
    
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    sending.value = false
    streamingMessage.value = ''
    await nextTick()
    scrollToBottom()
  }
}

const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

// 监听消息变化，自动滚动到底部
watch(currentMessages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })
</script>

<style scoped>
.chat-interface {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
}

.sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h2 {
  margin: 0 0 1rem 0;
  color: #4a72ff;
}

.new-chat-btn {
  width: 100%;
  padding: 0.75rem;
  background: #4a72ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.new-chat-btn:hover {
  background: #4366e8;
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.conversation-item {
  padding: 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 0.25rem;
  transition: background-color 0.2s;
}

.conversation-item:hover {
  background: #f0f0f0;
}

.conversation-item.active {
  background: #e3f2fd;
  border-left: 3px solid #4a72ff;
}

.conversation-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conversation-time {
  font-size: 0.8rem;
  color: #666;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-btn {
  padding: 0.25rem 0.5rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.welcome-screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.welcome-screen h1 {
  color: #4a72ff;
  margin-bottom: 1rem;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  position: relative;
}

.message.user .message-content {
  background: #4a72ff;
  color: white;
}

.message.assistant .message-content {
  background: white;
  border: 1px solid #e0e0e0;
}

.message-text {
  line-height: 1.5;
}

.message-time {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.25rem;
}

.typing-indicator {
  color: #666;
  font-style: italic;
  margin-top: 0.5rem;
}

.input-area {
  padding: 1rem;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-options {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.input-options label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  color: #666;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
}

.input-container textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: none;
  font-family: inherit;
  font-size: 1rem;
  min-height: 44px;
  max-height: 120px;
}

.input-container textarea:focus {
  outline: none;
  border-color: #4a72ff;
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: #4a72ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  white-space: nowrap;
}

.send-btn:hover:not(:disabled) {
  background: #4366e8;
}

.send-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
