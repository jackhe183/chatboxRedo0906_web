<template>
  <div class="login-view">
    <el-card class="login-card" shadow="always">
      <div class="login-header">
        <div class="logo">
          <el-icon size="48" color="#409EFF">
            <ChatDotRound />
          </el-icon>
          <h1>DeepSeek ChatBox</h1>
          <p>智能对话助手</p>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="login-tabs">
        <el-tab-pane label="登录" name="login">
          <el-form 
            :model="loginForm" 
            :rules="loginRules" 
            ref="loginFormRef"
            label-position="top"
            @submit.prevent="handleLogin"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :disabled="loading"
                size="large"
                prefix-icon="User"
              />
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                show-password
                :disabled="loading"
                size="large"
                prefix-icon="Lock"
              />
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                :loading="loading"
                @click="handleLogin"
                class="submit-btn"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form 
            :model="registerForm" 
            :rules="registerRules" 
            ref="registerFormRef"
            label-position="top"
            @submit.prevent="handleRegister"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名"
                :disabled="loading"
                size="large"
                prefix-icon="User"
              />
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码"
                show-password
                :disabled="loading"
                size="large"
                prefix-icon="Lock"
              />
            </el-form-item>

            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                show-password
                :disabled="loading"
                size="large"
                prefix-icon="Lock"
              />
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                size="large" 
                :loading="loading"
                @click="handleRegister"
                class="submit-btn"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import { ChatDotRound } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('login')
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const loginFormRef = ref(null)
const registerFormRef = ref(null)

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.login(loginForm.username, loginForm.password)
    
    if (result.success) {
      ElMessage.success('登录成功')
      router.push('/chat')
    } else {
      ElMessage.error(result.error || '登录失败')
    }
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.register(registerForm.username, registerForm.password)
    
    if (result.success) {
      ElMessage.success('注册成功，正在自动登录...')
      // 注册成功后自动登录
      const loginResult = await authStore.login(registerForm.username, registerForm.password)
      if (loginResult.success) {
        router.push('/chat')
      } else {
        ElMessage.error('自动登录失败，请手动登录')
      }
    } else {
      ElMessage.error(result.error || '注册失败')
    }
  } catch (error) {
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  border-radius: 16px;
  overflow: hidden;
}

.login-header {
  text-align: center;
  padding: 32px 0 24px 0;
  border-bottom: 1px solid #f0f0f0;
}

.logo h1 {
  margin: 16px 0 8px 0;
  color: #409EFF;
  font-size: 24px;
  font-weight: 600;
}

.logo p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.login-tabs {
  padding: 24px;
}

.login-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.login-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.login-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-view {
    padding: 10px;
  }
  
  .login-card {
    max-width: 100%;
  }
  
  .login-header {
    padding: 24px 0 16px 0;
  }
  
  .logo h1 {
    font-size: 20px;
  }
  
  .login-tabs {
    padding: 16px;
  }
}
</style>
