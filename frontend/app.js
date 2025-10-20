// ChatBox 应用主逻辑
class ChatBoxApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000/api';
        this.token = localStorage.getItem('token') || '';
        this.currentConversation = null;
        this.conversations = [];
        this.messages = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuth();
        this.setupMarkdown();
    }

    setupEventListeners() {
        // 登录/注册切换
        document.getElementById('loginTab').addEventListener('click', () => this.switchTab('login'));
        document.getElementById('registerTab').addEventListener('click', () => this.switchTab('register'));
        
        // 表单提交
        document.getElementById('authForm').addEventListener('submit', (e) => this.handleAuth(e));
        
        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());
        
        // 新对话
        document.getElementById('newChatBtn').addEventListener('click', () => this.createNewConversation());
        
        // 发送消息
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('messageInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    setupMarkdown() {
        // 配置 marked
        marked.setOptions({
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value;
                    } catch (err) {
                        console.error('代码高亮失败:', err);
                    }
                }
                return hljs.highlightAuto(code).value;
            },
            breaks: true,
            gfm: true
        });
    }

    checkAuth() {
        if (this.token) {
            this.showApp();
            this.fetchUserInfo();
            this.fetchConversations();
        } else {
            this.showLogin();
        }
    }

    switchTab(tab) {
        const loginTab = document.getElementById('loginTab');
        const registerTab = document.getElementById('registerTab');
        const submitBtn = document.getElementById('submitBtn');
        
        if (tab === 'login') {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            submitBtn.textContent = '登录';
        } else {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            submitBtn.textContent = '注册';
        }
    }

    async handleAuth(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const isLogin = document.getElementById('loginTab').classList.contains('active');
        
        if (!username || !password) {
            this.showError('请填写完整信息');
            return;
        }

        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.textContent = '处理中...';

        try {
            let result;
            if (isLogin) {
                result = await this.login(username, password);
            } else {
                result = await this.register(username, password);
                if (result.success) {
                    result = await this.login(username, password);
                }
            }

            if (result.success) {
                this.showApp();
                this.fetchUserInfo();
                this.fetchConversations();
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('网络错误，请重试');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = isLogin ? '登录' : '注册';
        }
    }

    async register(username, password) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.detail || '注册失败' };
            }
        } catch (error) {
            return { success: false, error: '网络错误' };
        }
    }

    async login(username, password) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                localStorage.setItem('token', this.token);
                return { success: true };
            } else {
                const error = await response.json();
                return { success: false, error: error.detail || '登录失败' };
            }
        } catch (error) {
            return { success: false, error: '网络错误' };
        }
    }

    async fetchUserInfo() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                document.getElementById('userName').textContent = user.username;
            }
        } catch (error) {
            console.error('获取用户信息失败:', error);
        }
    }

    async fetchConversations() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/conversations/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.conversations = data.conversations;
                this.renderConversations();
            }
        } catch (error) {
            console.error('获取会话列表失败:', error);
        }
    }

    renderConversations() {
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';

        if (this.conversations.length === 0) {
            historyList.innerHTML = '<div style="text-align: center; color: #666; padding: 1rem;">暂无历史对话</div>';
            return;
        }

        // 按时间分组
        const today = new Date();
        const todayStr = today.toDateString();
        const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);

        const todayConvs = [];
        const weekConvs = [];
        const monthConvs = [];

        this.conversations.forEach(conv => {
            const convDate = new Date(conv.updated_at);
            if (convDate.toDateString() === todayStr) {
                todayConvs.push(conv);
            } else if (convDate > weekAgo) {
                weekConvs.push(conv);
            } else if (convDate > monthAgo) {
                monthConvs.push(conv);
            }
        });

        if (todayConvs.length > 0) {
            this.renderConversationGroup('今天', todayConvs, historyList);
        }
        if (weekConvs.length > 0) {
            this.renderConversationGroup('7 天内', weekConvs, historyList);
        }
        if (monthConvs.length > 0) {
            this.renderConversationGroup('30 天内', monthConvs, historyList);
        }
    }

    renderConversationGroup(title, conversations, container) {
        const groupDiv = document.createElement('div');
        groupDiv.innerHTML = `
            <div class="history-group-title">${title}</div>
        `;

        conversations.forEach(conv => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'history-item';
            itemDiv.textContent = conv.title;
            itemDiv.addEventListener('click', () => this.selectConversation(conv));
            groupDiv.appendChild(itemDiv);
        });

        container.appendChild(groupDiv);
    }

    async createNewConversation() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/conversations/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ title: '新对话' })
            });

            if (response.ok) {
                const conversation = await response.json();
                this.conversations.unshift(conversation);
                this.renderConversations();
                this.selectConversation(conversation);
            }
        } catch (error) {
            console.error('创建会话失败:', error);
        }
    }

    async selectConversation(conversation) {
        this.currentConversation = conversation;
        
        // 更新UI状态
        document.querySelectorAll('.history-item').forEach(item => {
            item.classList.remove('active');
        });
        event.target.classList.add('active');

        // 显示聊天界面
        document.getElementById('welcomeScreen').classList.add('hidden');
        document.getElementById('chatContainer').classList.add('active');

        // 加载消息
        await this.fetchMessages(conversation.id);
    }

    async fetchMessages(conversationId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/messages/conversation/${conversationId}`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.messages = data.messages;
                this.renderMessages();
            }
        } catch (error) {
            console.error('获取消息失败:', error);
        }
    }

    renderMessages() {
        const container = document.getElementById('messagesContainer');
        container.innerHTML = '';

        this.messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message.role}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            const textDiv = document.createElement('div');
            textDiv.className = 'message-text';
            
            if (message.role === 'assistant') {
                textDiv.innerHTML = marked.parse(message.content);
            } else {
                textDiv.textContent = message.content;
            }
            
            const timeDiv = document.createElement('div');
            timeDiv.className = 'message-time';
            timeDiv.textContent = this.formatTime(message.created_at);
            
            contentDiv.appendChild(textDiv);
            contentDiv.appendChild(timeDiv);
            messageDiv.appendChild(contentDiv);
            container.appendChild(messageDiv);
        });

        this.scrollToBottom();
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message || !this.currentConversation) return;

        input.value = '';
        
        // 添加用户消息到界面
        this.addMessageToUI('user', message);
        
        // 显示AI正在输入
        this.showTypingIndicator();

        try {
            const enableSearch = document.getElementById('enableSearch').checked;
            const enableThinking = document.getElementById('enableThinking').checked;

            const response = await fetch(`${this.apiBaseUrl}/messages/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    content: message,
                    conversation_id: this.currentConversation.id,
                    enable_search: enableSearch,
                    enable_thinking: enableThinking
                })
            });

            if (response.ok) {
                // 处理流式响应
                await this.handleStreamResponse(response);
            } else {
                this.showError('发送消息失败');
            }
        } catch (error) {
            console.error('发送消息失败:', error);
            this.showError('网络错误');
        } finally {
            this.hideTypingIndicator();
        }
    }

    async handleStreamResponse(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let aiMessage = '';

        // 移除打字指示器
        this.hideTypingIndicator();

        // 添加AI消息容器
        const messageDiv = this.addMessageToUI('assistant', '');
        const textDiv = messageDiv.querySelector('.message-text');

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'content' && data.content) {
                                aiMessage += data.content;
                                textDiv.innerHTML = marked.parse(aiMessage);
                                this.scrollToBottom();
                            } else if (data.type === 'done') {
                                break;
                            }
                        } catch (e) {
                            // 忽略解析错误
                        }
                    }
                }
            }
        } catch (error) {
            console.error('处理流式响应失败:', error);
        }
    }

    addMessageToUI(role, content) {
        const container = document.getElementById('messagesContainer');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        
        if (role === 'assistant') {
            textDiv.innerHTML = marked.parse(content);
        } else {
            textDiv.textContent = content;
        }
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date().toISOString());
        
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        container.appendChild(messageDiv);
        
        this.scrollToBottom();
        return messageDiv;
    }

    showTypingIndicator() {
        const container = document.getElementById('messagesContainer');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">正在思考...</div>
                <div class="typing-indicator">AI正在输入</div>
            </div>
        `;
        container.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingDiv = document.getElementById('typingIndicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    scrollToBottom() {
        const container = document.getElementById('messagesContainer');
        container.scrollTop = container.scrollHeight;
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    }

    showLogin() {
        document.getElementById('loginPage').classList.remove('hidden');
        document.getElementById('appPage').classList.add('hidden');
    }

    showApp() {
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('appPage').classList.remove('hidden');
    }

    logout() {
        this.token = '';
        localStorage.removeItem('token');
        this.currentConversation = null;
        this.conversations = [];
        this.messages = [];
        this.showLogin();
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    new ChatBoxApp();
});
