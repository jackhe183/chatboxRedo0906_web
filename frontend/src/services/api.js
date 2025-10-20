import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理认证错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      // 可以在这里添加路由跳转到登录页
    }
    return Promise.reject(error)
  }
)

// ==================== 用户相关API ====================
export const userApi = {
  // 用户注册
  register: async (username, password) => {
    const response = await api.post('/users/register', {
      username,
      password
    })
    return response.data
  },

  // 用户登录
  login: async (username, password) => {
    const response = await api.post('/users/login', {
      username,
      password
    })
    return response.data
  },

  // 获取当前用户信息
  getCurrentUser: async () => {
    const response = await api.get('/users/me')
    return response.data
  },

  // 更新用户信息
  updateUser: async (userData) => {
    const response = await api.put('/users/me', userData)
    return response.data
  },

  // 删除用户账户
  deleteUser: async () => {
    const response = await api.delete('/users/me')
    return response.data
  }
}

// ==================== 会话相关API ====================
export const conversationApi = {
  // 获取会话列表
  getConversations: async () => {
    const response = await api.get('/conversations/')
    return response.data
  },

  // 创建新会话
  createConversation: async (title = '新对话') => {
    const response = await api.post('/conversations/', { title })
    return response.data
  },

  // 获取特定会话
  getConversation: async (conversationId) => {
    const response = await api.get(`/conversations/${conversationId}`)
    return response.data
  },

  // 更新会话标题
  updateConversation: async (conversationId, title) => {
    const response = await api.put(`/conversations/${conversationId}`, { title })
    return response.data
  },

  // 删除会话
  deleteConversation: async (conversationId) => {
    const response = await api.delete(`/conversations/${conversationId}`)
    return response.data
  }
}

// ==================== 消息相关API ====================
export const messageApi = {
  // 获取会话消息
  getMessages: async (conversationId) => {
    const response = await api.get(`/messages/conversation/${conversationId}`)
    return response.data
  },

  // 更新消息内容
  updateMessage: async (messageId, content) => {
    const response = await api.put(`/messages/${messageId}`, { content })
    return response.data
  },

  // 删除消息
  deleteMessage: async (messageId) => {
    const response = await api.delete(`/messages/${messageId}`)
    return response.data
  }
}

// ==================== 流式API ====================
export const streamApi = {
  sendMessage: async (messageData, onChunk, onError, onComplete) => {
    const authStore = useAuthStore()
    const token = authStore.token
    
    try {
      const response = await fetch(`${API_BASE_URL}/messages/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(messageData)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        
        if (done) {
          onComplete?.()
          break
        }

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              onChunk?.(data)
            } catch (e) {
              console.error('解析流式数据失败:', e)
            }
          }
        }
      }
    } catch (error) {
      onError?.(error)
    }
  }
}

// ==================== 错误处理工具 ====================
export const handleApiError = (error) => {
  if (error.response) {
    // 服务器响应了错误状态码
    const { status, data } = error.response
    return {
      message: data?.detail || `请求失败 (${status})`,
      status,
      data
    }
  } else if (error.request) {
    // 请求已发出但没有收到响应
    return {
      message: '网络连接失败，请检查网络设置',
      status: 0
    }
  } else {
    // 其他错误
    return {
      message: error.message || '未知错误',
      status: -1
    }
  }
}

// ==================== 类型定义 ====================
/**
 * @typedef {Object} User
 * @property {number} id - 用户ID
 * @property {string} username - 用户名
 * @property {string} created_at - 创建时间
 */

/**
 * @typedef {Object} Conversation
 * @property {number} id - 会话ID
 * @property {string} title - 会话标题
 * @property {string} created_at - 创建时间
 * @property {string} updated_at - 更新时间
 * @property {number} message_count - 消息数量
 */

/**
 * @typedef {Object} Message
 * @property {number} id - 消息ID
 * @property {string} role - 角色 (user/assistant)
 * @property {string} content - 消息内容
 * @property {string} status - 状态 (completed/processing/failed)
 * @property {string} created_at - 创建时间
 */

/**
 * @typedef {Object} StreamChunk
 * @property {string} type - 类型 (content/thinking/done/error/conversation/message)
 * @property {string} [content] - 内容
 * @property {number} [conversation_id] - 会话ID
 * @property {number} [message_id] - 消息ID
 */

export default api