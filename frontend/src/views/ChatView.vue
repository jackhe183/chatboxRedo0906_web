<template>
  <div class="chat-view">
    <el-container style="height: 100vh;">
      <!-- 左侧边栏 -->
      <el-aside :width="sidebarCollapsed ? '64px' : '260px'" class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <el-icon size="24" color="#409EFF">
              <ChatDotRound />
            </el-icon>
            <span v-show="!sidebarCollapsed">DeepSeek ChatBox</span>
          </div>
          <el-button 
            :icon="sidebarCollapsed ? Expand : Fold" 
            text 
            circle 
            @click="toggleSidebar"
          />
        </div>

        <div class="sidebar-content">
          <el-button 
            class="new-chat-btn" 
            :icon="Plus" 
            @click="createNewConversation" 
            :disabled="sidebarCollapsed"
            type="primary"
          >
            开启新对话
          </el-button>

          <el-scrollbar class="history-list">
            <el-menu 
              :default-active="currentConversationId?.toString()" 
              @select="loadConversation" 
              :collapse="sidebarCollapsed"
            >
              <el-menu-item-group v-for="group in conversationGroups" :key="group.title" :title="group.title">
                <el-menu-item 
                  v-for="conversation in group.conversations" 
                  :key="conversation.id" 
                  :index="conversation.id.toString()"
                >
                  <el-icon><ChatDotRound /></el-icon>
                  <template #title>{{ conversation.title }}</template>
                </el-menu-item>
              </el-menu-item-group>
            </el-menu>
          </el-scrollbar>
        </div>

        <div class="sidebar-footer">
          <div class="user-profile">
            <el-avatar size="small" style="background-color: #409EFF">
              {{ user?.username?.charAt(0).toUpperCase() || 'U' }}
            </el-avatar>
            <span v-show="!sidebarCollapsed">{{ user?.username }}</span>
          </div>
          <el-dropdown v-show="!sidebarCollapsed" trigger="click">
            <el-button :icon="MoreFilled" text circle />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-aside>

      <!-- 右侧主聊天区 -->
      <el-main class="chat-area">
        <!-- 功能开关 -->
        <div class="feature-toggles">
          <el-check-tag 
            :checked="features.deepThinking" 
            @change="toggleFeature('deepThinking')"
            class="feature-tag"
          >
            🧠 深度思考
          </el-check-tag>
          <el-check-tag 
            :checked="features.webSearch" 
            @change="toggleFeature('webSearch')"
            class="feature-tag"
          >
            🌐 联网搜索
          </el-check-tag>
        </div>

        <!-- 聊天消息或欢迎界面 -->
        <el-scrollbar v-if="currentMessages.length > 0" class="chat-messages" ref="messagesScrollbar">
          <div ref="messagesContainer">
            <div 
              v-for="message in currentMessages" 
              :key="message.id" 
              class="message" 
              :class="message.role"
            >
              <div class="message-avatar">
                {{ message.role === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="message-content">
                <div class="message-text" v-html="renderMarkdown(message.content)"></div>
                <div class="message-time">{{ formatTime(message.created_at) }}</div>
              </div>
            </div>
            
            <!-- 流式消息显示 -->
            <div v-if="streamingMessage" class="message assistant">
              <div class="message-avatar">🤖</div>
              <div class="message-content">
                <div class="message-text" v-html="renderMarkdown(streamingMessage)"></div>
                <div class="typing-indicator">
                  <el-icon class="is-loading"><Loading /></el-icon>
                  正在输入...
                </div>
              </div>
            </div>
          </div>
        </el-scrollbar>
        
        <div v-else class="welcome-screen">
          <div class="welcome-content">
            <div class="logo">
              <el-icon size="48" color="#409EFF">
                <ChatDotRound />
              </el-icon>
            </div>
            <h1>今天有什么可以帮到你?</h1>
            <p>开始一个新的对话，体验智能AI助手</p>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-wrapper">
          <div class="input-box">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :autosize="{ minRows: 1, maxRows: 5 }"
              placeholder="给 DeepSeek 发送消息"
              @keydown.enter.prevent="handleSendMessage"
              :disabled="sending"
            />
            <el-button
              class="send-button"
              type="primary"
              circle
              :icon="Promotion"
              @click="handleSendMessage"
              :disabled="!inputMessage.trim() || sending"
              :loading="sending"
            />
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useChatStore } from '../stores/chat'
import { renderMarkdown } from '../utils/markdown'
import { ElMessage } from 'element-plus'
import { 
  ChatDotRound, 
  Expand, 
  Fold, 
  Plus, 
  MoreFilled, 
  Loading, 
  Promotion 
} from '@element-plus/icons-vue'

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

// 响应式数据
const sidebarCollapsed = ref(false)
const inputMessage = ref('')
const sending = ref(false)
const streamingMessage = ref('')
const features = ref({ 
  deepThinking: false, 
  webSearch: false 
})

const messagesScrollbar = ref(null)
const messagesContainer = ref(null)

// 计算属性
const currentConversationId = computed(() => currentConversation.value?.id)

const conversationGroups = computed(() => {
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  
  const groups = {
    '今天': [],
    '昨天': [],
    '更早': []
  }
  
  conversations.value.forEach(conv => {
    const convDate = new Date(conv.updated_at)
    if (convDate.toDateString() === today.toDateString()) {
      groups['今天'].push(conv)
    } else if (convDate.toDateString() === yesterday.toDateString()) {
      groups['昨天'].push(conv)
    } else {
      groups['更早'].push(conv)
    }
  })
  
  return Object.entries(groups)
    .filter(([_, convs]) => convs.length > 0)
    .map(([title, conversations]) => ({ title, conversations }))
})

// 方法
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const toggleFeature = (feature) => {
  features.value[feature] = !features.value[feature]
}

const createNewConversation = async () => {
  try {
    const newConversation = await chatStore.createConversation()
    await chatStore.selectConversation(newConversation)
  } catch (error) {
    ElMessage.error('创建新对话失败')
  }
}

const loadConversation = async (conversationId) => {
  if (!conversationId) return
  const conversation = conversations.value.find(c => c.id === parseInt(conversationId))
  if (conversation) {
    await chatStore.selectConversation(conversation)
  }
}

const handleSendMessage = async () => {
  if (!inputMessage.value.trim() || sending.value) return

  const message = inputMessage.value.trim()
  inputMessage.value = ''
  sending.value = true
  streamingMessage.value = ''

  // 添加用户消息到界面
  const userMessage = {
    id: Date.now(),
    conversation_id: currentConversation.value?.id,
    role: 'user',
    content: message,
    status: 'completed',
    created_at: new Date().toISOString()
  }
  messages.value.push(userMessage)

  try {
    await chatStore.sendMessage(
      message, 
      features.value.webSearch, 
      features.value.deepThinking,
      (chunk) => {
        // 处理流式数据
        if (chunk.type === 'content' || chunk.type === 'thinking') {
          streamingMessage.value += chunk.content || ''
        }
      },
      (error) => {
        ElMessage.error('发送消息失败: ' + error.message)
        streamingMessage.value = ''
      },
      () => {
        // 完成时，将流式消息添加到消息列表
        if (streamingMessage.value) {
          const aiMessage = {
            id: Date.now() + 1,
            conversation_id: currentConversation.value?.id,
            role: 'assistant',
            content: streamingMessage.value,
            status: 'completed',
            created_at: new Date().toISOString()
          }
          messages.value.push(aiMessage)
          streamingMessage.value = ''
        }
        sending.value = false
        scrollToBottom()
      }
    )
  } catch (error) {
    ElMessage.error('发送消息失败')
    sending.value = false
    streamingMessage.value = ''
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollbar.value && messagesContainer.value) {
      messagesScrollbar.value.setScrollTop(messagesContainer.value.scrollHeight)
    }
  })
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

// 生命周期钩子
onMounted(async () => {
  await chatStore.fetchConversations()
})

// 监听消息变化，自动滚动到底部
watch([currentMessages, streamingMessage], () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })
</script>

<style scoped>
.chat-view {
  height: 100vh;
  background: #f5f5f5;
}

.sidebar {
  background: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #409EFF;
}

.sidebar-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
}

.new-chat-btn {
  width: 100%;
  height: 40px;
}

.history-list {
  flex: 1;
  min-height: 0;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-area {
  display: flex;
  flex-direction: column;
  padding: 0;
  background: #f5f5f5;
}

.feature-toggles {
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.feature-tag {
  margin-right: 8px;
}

.chat-messages {
  flex: 1;
  padding: 24px;
}

.message {
  display: flex;
  margin-bottom: 24px;
  gap: 12px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #409EFF;
  color: white;
}

.message.assistant .message-avatar {
  background: #f0f0f0;
  color: #666;
}

.message-content {
  max-width: 70%;
  min-width: 200px;
}

.message.user .message-content {
  text-align: right;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
}

.message.user .message-text {
  background: #409EFF;
  color: white;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #999;
  font-size: 14px;
  margin-top: 8px;
}

.welcome-screen {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  margin: 24px;
  border-radius: 12px;
}

.welcome-content {
  text-align: center;
}

.welcome-content h1 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 24px;
  font-weight: 500;
}

.welcome-content p {
  color: #666;
  font-size: 16px;
}

.input-wrapper {
  padding: 24px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-box {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  max-width: 800px;
  margin: 0 auto;
}

.send-button {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    z-index: 1000;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.3s;
  }
  
  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style>
