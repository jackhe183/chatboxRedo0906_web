<template>
  <div class="login-container">
    <div class="login-form">
      <div class="logo">
        <h1>ChatBox</h1>
        <p>智能对话助手</p>
      </div>
      
      <div class="form-tabs">
        <button 
          :class="{ active: isLogin }" 
          @click="isLogin = true"
        >
          登录
        </button>
        <button 
          :class="{ active: !isLogin }" 
          @click="isLogin = false"
        >
          注册
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <input
            v-model="form.username"
            type="text"
            placeholder="用户名"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <input
            v-model="form.password"
            type="password"
            placeholder="密码"
            required
            :disabled="loading"
          />
        </div>

        <button 
          type="submit" 
          class="submit-btn"
          :disabled="loading"
        >
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  if (!form.username || !form.password) {
    error.value = '请填写完整信息'
    return
  }

  loading.value = true
  error.value = ''

  try {
    let result
    if (isLogin.value) {
      result = await authStore.login(form.username, form.password)
    } else {
      result = await authStore.register(form.username, form.password)
      if (result.success) {
        // 注册成功后自动登录
        result = await authStore.login(form.username, form.password)
      }
    }

    if (result.success) {
      router.push('/chat')
    } else {
      error.value = result.error
    }
  } catch (err) {
    error.value = '网络错误，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.logo {
  text-align: center;
  margin-bottom: 2rem;
}

.logo h1 {
  color: #4a72ff;
  margin: 0;
  font-size: 2rem;
}

.logo p {
  color: #666;
  margin: 0.5rem 0 0 0;
}

.form-tabs {
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.form-tabs button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.form-tabs button.active {
  color: #4a72ff;
  border-bottom-color: #4a72ff;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #4a72ff;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background: #4a72ff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #4366e8;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fee;
  color: #c33;
  border-radius: 6px;
  text-align: center;
}
</style>
