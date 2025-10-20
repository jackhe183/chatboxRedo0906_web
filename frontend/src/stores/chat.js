import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { conversationApi, messageApi, streamApi, handleApiError } from '../services/api'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([])
  const currentConversation = ref(null)
  const messages = ref([])
  const loading = ref(false)

  const currentMessages = computed(() => {
    if (!currentConversation.value) return []
    return messages.value.filter(msg => 
      msg.conversation_id === currentConversation.value.id
    )
  })

  const fetchConversations = async () => {
    loading.value = true
    try {
      const response = await conversationApi.getConversations()
      conversations.value = response.conversations
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('获取会话列表失败:', errorInfo.message)
      throw errorInfo
    } finally {
      loading.value = false
    }
  }

  const createConversation = async (title = '新对话') => {
    try {
      const newConversation = await conversationApi.createConversation(title)
      conversations.value.unshift(newConversation)
      return newConversation
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('创建会话失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const selectConversation = async (conversation) => {
    currentConversation.value = conversation
    await fetchMessages(conversation.id)
  }

  const fetchMessages = async (conversationId) => {
    try {
      const response = await messageApi.getMessages(conversationId)
      messages.value = response.messages
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('获取消息失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const sendMessage = async (content, enableSearch = false, enableThinking = false, onChunk, onError, onComplete) => {
    if (!content.trim()) return

    const messageData = {
      content: content.trim(),
      enable_search: enableSearch,
      enable_thinking: enableThinking
    }

    // 如果有当前会话，添加到现有会话
    if (currentConversation.value) {
      messageData.conversation_id = currentConversation.value.id
    }

    try {
      await streamApi.sendMessage(
        messageData,
        (chunk) => {
          // 处理流式数据
          if (chunk.type === 'conversation') {
            // 新会话创建
            currentConversation.value = {
              id: chunk.conversation_id,
              title: '新对话',
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              message_count: 0
            }
            conversations.value.unshift(currentConversation.value)
          } else if (chunk.type === 'message') {
            // 新消息创建
            const newMessage = {
              id: chunk.message_id,
              conversation_id: currentConversation.value?.id,
              role: 'assistant',
              content: '',
              status: 'processing',
              created_at: new Date().toISOString()
            }
            messages.value.push(newMessage)
          } else if (chunk.type === 'content' || chunk.type === 'thinking') {
            // 更新最后一条消息内容
            const lastMessage = messages.value[messages.value.length - 1]
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.content += chunk.content || ''
            }
          } else if (chunk.type === 'done') {
            // 完成
            const lastMessage = messages.value[messages.value.length - 1]
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.status = 'completed'
            }
          } else if (chunk.type === 'error') {
            // 错误处理
            const lastMessage = messages.value[messages.value.length - 1]
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.status = 'failed'
              lastMessage.content = chunk.content || '发送失败'
            }
          }
          
          onChunk?.(chunk)
        },
        (error) => {
          const errorInfo = handleApiError(error)
          console.error('发送消息失败:', errorInfo.message)
          onError?.(errorInfo)
        },
        () => {
          onComplete?.()
        }
      )
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('发送消息失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const updateConversationTitle = async (conversationId, title) => {
    try {
      const updatedConversation = await conversationApi.updateConversation(conversationId, title)
      
      // 更新本地会话列表
      const index = conversations.value.findIndex(conv => conv.id === conversationId)
      if (index !== -1) {
        conversations.value[index] = updatedConversation
      }
      
      // 如果当前会话被更新，也更新当前会话
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = updatedConversation
      }
      
      return updatedConversation
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('更新会话标题失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const updateMessageContent = async (messageId, content) => {
    try {
      const updatedMessage = await messageApi.updateMessage(messageId, content)
      
      // 更新本地消息列表
      const index = messages.value.findIndex(msg => msg.id === messageId)
      if (index !== -1) {
        messages.value[index] = updatedMessage
      }
      
      return updatedMessage
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('更新消息内容失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const deleteConversation = async (conversationId) => {
    try {
      await conversationApi.deleteConversation(conversationId)
      conversations.value = conversations.value.filter(
        conv => conv.id !== conversationId
      )
      
      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = null
        messages.value = []
      }
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('删除会话失败:', errorInfo.message)
      throw errorInfo
    }
  }

  const deleteMessage = async (messageId) => {
    try {
      await messageApi.deleteMessage(messageId)
      messages.value = messages.value.filter(msg => msg.id !== messageId)
    } catch (error) {
      const errorInfo = handleApiError(error)
      console.error('删除消息失败:', errorInfo.message)
      throw errorInfo
    }
  }

  return {
    conversations,
    currentConversation,
    messages,
    loading,
    currentMessages,
    fetchConversations,
    createConversation,
    selectConversation,
    fetchMessages,
    sendMessage,
    updateConversationTitle,
    updateMessageContent,
    deleteConversation,
    deleteMessage
  }
})