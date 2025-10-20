import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi, handleApiError } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username, password) => {
    loading.value = true
    try {
      const response = await userApi.login(username, password)
      
      token.value = response.access_token
      localStorage.setItem('token', token.value)
      
      // 获取用户信息
      await fetchUserInfo()
      
      return { success: true }
    } catch (error) {
      const errorInfo = handleApiError(error)
      return { 
        success: false, 
        error: errorInfo.message
      }
    } finally {
      loading.value = false
    }
  }

  const register = async (username, password) => {
    loading.value = true
    try {
      await userApi.register(username, password)
      return { success: true }
    } catch (error) {
      const errorInfo = handleApiError(error)
      return { 
        success: false, 
        error: errorInfo.message
      }
    } finally {
      loading.value = false
    }
  }

  const fetchUserInfo = async () => {
    if (!token.value) return
    
    try {
      const userData = await userApi.getCurrentUser()
      user.value = userData
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取用户信息失败，可能是token过期，清除认证状态
      if (error.response?.status === 401) {
        logout()
      }
    }
  }

  const updateUserInfo = async (userData) => {
    loading.value = true
    try {
      const response = await userApi.updateUser(userData)
      
      // 如果返回了新的token，更新token
      if (response.access_token) {
        token.value = response.access_token
        localStorage.setItem('token', token.value)
      }
      
      // 更新用户信息
      user.value = {
        id: response.id,
        username: response.username,
        created_at: response.created_at
      }
      
      return { success: true }
    } catch (error) {
      const errorInfo = handleApiError(error)
      return { 
        success: false, 
        error: errorInfo.message
      }
    } finally {
      loading.value = false
    }
  }

  const deleteAccount = async () => {
    loading.value = true
    try {
      await userApi.deleteUser()
      logout()
      return { success: true }
    } catch (error) {
      const errorInfo = handleApiError(error)
      return { 
        success: false, 
        error: errorInfo.message
      }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    login,
    register,
    fetchUserInfo,
    updateUserInfo,
    deleteAccount,
    logout
  }
})