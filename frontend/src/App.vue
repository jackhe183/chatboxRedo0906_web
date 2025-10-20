<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  // 检查是否已登录
  if (authStore.isAuthenticated) {
    await authStore.fetchUserInfo()
    if (router.currentRoute.value.path === '/login') {
      router.push('/chat')
    }
  } else if (router.currentRoute.value.path === '/chat') {
    router.push('/login')
  }
})
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  height: 100vh;
  overflow: hidden;
}

/* 代码高亮样式 */
.hljs {
  background: #f8f8f8 !important;
  border-radius: 4px;
  padding: 0.5rem;
  margin: 0.5rem 0;
}

/* Markdown 样式 */
.message-text h1,
.message-text h2,
.message-text h3 {
  margin: 1rem 0 0.5rem 0;
}

.message-text p {
  margin: 0.5rem 0;
}

.message-text ul,
.message-text ol {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.message-text code {
  background: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.message-text pre {
  background: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.message-text blockquote {
  border-left: 4px solid #4a72ff;
  padding-left: 1rem;
  margin: 0.5rem 0;
  color: #666;
}
</style>