#!/usr/bin/env python3
"""
API测试文件 - 测试所有16个API接口
包括原有的12个接口和新增的4个CRUD接口
"""

import requests
import json
import time
from typing import Dict, Any

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser123",
    "password": "testpass123"
}
TEST_USER_UPDATE = {
    "username": "testuser456",
    "password": "newpass123"
}

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.conversation_id = None
        self.message_id = None
        
    def log(self, message: str, status: str = "INFO"):
        """打印日志"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{status}] {message}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> requests.Response:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"请求失败: {e}", "ERROR")
            raise
    
    def test_health_check(self):
        """测试健康检查接口"""
        self.log("=== 测试健康检查接口 ===")
        
        # 测试根路径
        response = self.make_request("GET", "/")
        self.log(f"GET / - 状态码: {response.status_code}")
        if response.status_code == 200:
            self.log("✅ 根路径健康检查通过")
        else:
            self.log("❌ 根路径健康检查失败", "ERROR")
        
        # 测试健康检查端点
        response = self.make_request("GET", "/health")
        self.log(f"GET /health - 状态码: {response.status_code}")
        if response.status_code == 200:
            self.log("✅ 健康检查端点通过")
        else:
            self.log("❌ 健康检查端点失败", "ERROR")
    
    def test_user_apis(self):
        """测试用户相关API"""
        self.log("=== 测试用户相关API ===")
        
        # 1. 用户注册
        self.log("1. 测试用户注册")
        response = self.make_request("POST", "/api/users/register", data=TEST_USER)
        self.log(f"POST /api/users/register - 状态码: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            self.user_id = user_data.get("id")
            self.log(f"✅ 用户注册成功，用户ID: {self.user_id}")
        else:
            self.log(f"❌ 用户注册失败: {response.text}", "ERROR")
            return False
        
        # 2. 用户登录
        self.log("2. 测试用户登录")
        response = self.make_request("POST", "/api/users/login", data=TEST_USER)
        self.log(f"POST /api/users/login - 状态码: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")
            self.log("✅ 用户登录成功，获取到Token")
        else:
            self.log(f"❌ 用户登录失败: {response.text}", "ERROR")
            return False
        
        # 3. 获取当前用户信息
        self.log("3. 测试获取当前用户信息")
        response = self.make_request("GET", "/api/users/me")
        self.log(f"GET /api/users/me - 状态码: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            self.log(f"✅ 获取用户信息成功: {user_info['username']}")
        else:
            self.log(f"❌ 获取用户信息失败: {response.text}", "ERROR")
        
        # 4. 更新用户信息
        self.log("4. 测试更新用户信息")
        response = self.make_request("PUT", "/api/users/me", data=TEST_USER_UPDATE)
        self.log(f"PUT /api/users/me - 状态码: {response.status_code}")
        if response.status_code == 200:
            updated_user = response.json()
            # 更新token（因为用户名可能已更改）
            if "access_token" in updated_user:
                self.token = updated_user["access_token"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            self.log(f"✅ 用户信息更新成功: {updated_user['username']}")
        else:
            self.log(f"❌ 用户信息更新失败: {response.text}", "ERROR")
        
        return True
    
    def test_conversation_apis(self):
        """测试会话相关API"""
        self.log("=== 测试会话相关API ===")
        
        # 1. 创建会话
        self.log("1. 测试创建会话")
        conversation_data = {"title": "测试会话"}
        response = self.make_request("POST", "/api/conversations/", data=conversation_data)
        self.log(f"POST /api/conversations/ - 状态码: {response.status_code}")
        if response.status_code == 200:
            conv_data = response.json()
            self.conversation_id = conv_data.get("id")
            self.log(f"✅ 会话创建成功，会话ID: {self.conversation_id}")
        else:
            self.log(f"❌ 会话创建失败: {response.text}", "ERROR")
            return False
        
        # 2. 获取会话列表
        self.log("2. 测试获取会话列表")
        response = self.make_request("GET", "/api/conversations/")
        self.log(f"GET /api/conversations/ - 状态码: {response.status_code}")
        if response.status_code == 200:
            conversations = response.json()
            self.log(f"✅ 获取会话列表成功，共 {len(conversations['conversations'])} 个会话")
        else:
            self.log(f"❌ 获取会话列表失败: {response.text}", "ERROR")
        
        # 3. 获取特定会话
        self.log("3. 测试获取特定会话")
        response = self.make_request("GET", f"/api/conversations/{self.conversation_id}")
        self.log(f"GET /api/conversations/{self.conversation_id} - 状态码: {response.status_code}")
        if response.status_code == 200:
            conv_info = response.json()
            self.log(f"✅ 获取会话信息成功: {conv_info['title']}")
        else:
            self.log(f"❌ 获取会话信息失败: {response.text}", "ERROR")
        
        # 4. 更新会话标题
        self.log("4. 测试更新会话标题")
        update_data = {"title": "更新后的会话标题"}
        response = self.make_request("PUT", f"/api/conversations/{self.conversation_id}", data=update_data)
        self.log(f"PUT /api/conversations/{self.conversation_id} - 状态码: {response.status_code}")
        if response.status_code == 200:
            updated_conv = response.json()
            self.log(f"✅ 会话标题更新成功: {updated_conv['title']}")
        else:
            self.log(f"❌ 会话标题更新失败: {response.text}", "ERROR")
        
        return True
    
    def test_message_apis(self):
        """测试消息相关API"""
        self.log("=== 测试消息相关API ===")
        
        # 1. 发送消息（创建用户消息）
        self.log("1. 测试发送消息")
        message_data = {
            "content": "这是一条测试消息",
            "conversation_id": self.conversation_id,
            "enable_search": False,
            "enable_thinking": False
        }
        response = self.make_request("POST", "/api/messages/send", data=message_data)
        self.log(f"POST /api/messages/send - 状态码: {response.status_code}")
        if response.status_code == 200:
            self.log("✅ 消息发送成功（流式响应）")
            # 注意：这里只测试了HTTP状态码，实际流式响应需要特殊处理
        else:
            self.log(f"❌ 消息发送失败: {response.text}", "ERROR")
        
        # 2. 获取会话消息
        self.log("2. 测试获取会话消息")
        response = self.make_request("GET", f"/api/messages/conversation/{self.conversation_id}")
        self.log(f"GET /api/messages/conversation/{self.conversation_id} - 状态码: {response.status_code}")
        if response.status_code == 200:
            messages = response.json()
            if messages['messages']:
                self.message_id = messages['messages'][0]['id']
                self.log(f"✅ 获取消息列表成功，共 {len(messages['messages'])} 条消息")
            else:
                self.log("⚠️ 消息列表为空")
        else:
            self.log(f"❌ 获取消息列表失败: {response.text}", "ERROR")
        
        # 3. 更新消息内容（如果存在用户消息）
        if self.message_id:
            self.log("3. 测试更新消息内容")
            update_data = {"content": "这是更新后的消息内容"}
            response = self.make_request("PUT", f"/api/messages/{self.message_id}", data=update_data)
            self.log(f"PUT /api/messages/{self.message_id} - 状态码: {response.status_code}")
            if response.status_code == 200:
                updated_msg = response.json()
                self.log(f"✅ 消息内容更新成功: {updated_msg['content']}")
            else:
                self.log(f"❌ 消息内容更新失败: {response.text}", "ERROR")
        
        # 4. 删除消息
        if self.message_id:
            self.log("4. 测试删除消息")
            response = self.make_request("DELETE", f"/api/messages/{self.message_id}")
            self.log(f"DELETE /api/messages/{self.message_id} - 状态码: {response.status_code}")
            if response.status_code == 200:
                self.log("✅ 消息删除成功")
            else:
                self.log(f"❌ 消息删除失败: {response.text}", "ERROR")
        
        return True
    
    def test_cleanup(self):
        """清理测试数据"""
        self.log("=== 清理测试数据 ===")
        
        # 删除会话
        if self.conversation_id:
            self.log("删除测试会话")
            response = self.make_request("DELETE", f"/api/conversations/{self.conversation_id}")
            if response.status_code == 200:
                self.log("✅ 测试会话删除成功")
            else:
                self.log(f"❌ 测试会话删除失败: {response.text}", "ERROR")
        
        # 删除用户账户
        self.log("删除测试用户账户")
        response = self.make_request("DELETE", "/api/users/me")
        if response.status_code == 200:
            self.log("✅ 测试用户账户删除成功")
        else:
            self.log(f"❌ 测试用户账户删除失败: {response.text}", "ERROR")
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("🚀 开始API测试", "INFO")
        self.log("=" * 50)
        
        try:
            # 1. 健康检查
            self.test_health_check()
            self.log("")
            
            # 2. 用户API测试
            if not self.test_user_apis():
                self.log("❌ 用户API测试失败，停止后续测试", "ERROR")
                return
            self.log("")
            
            # 3. 会话API测试
            if not self.test_conversation_apis():
                self.log("❌ 会话API测试失败，停止后续测试", "ERROR")
                return
            self.log("")
            
            # 4. 消息API测试
            if not self.test_message_apis():
                self.log("❌ 消息API测试失败", "ERROR")
            self.log("")
            
            # 5. 清理测试数据
            self.test_cleanup()
            
        except Exception as e:
            self.log(f"测试过程中发生异常: {e}", "ERROR")
        
        self.log("=" * 50)
        self.log("🏁 API测试完成", "INFO")

def main():
    """主函数"""
    print("API测试工具 - 测试所有16个接口")
    print("确保后端服务已启动在 http://localhost:8000")
    print("按回车键开始测试...")
    input()
    
    tester = APITester(BASE_URL)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
