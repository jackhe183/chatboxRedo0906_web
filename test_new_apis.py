#!/usr/bin/env python3
"""
测试新增的4个CRUD API接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_new_apis():
    """测试新增的4个API接口"""
    
    # 测试用户数据
    test_user = {
        "username": "newtestuser",
        "password": "newtestpass123"
    }
    
    test_user_update = {
        "username": "updateduser",
        "password": "updatedpass123"
    }
    
    session = requests.Session()
    token = None
    conversation_id = None
    message_id = None
    
    print("🚀 开始测试新增的4个CRUD API接口")
    print("=" * 60)
    
    try:
        # 1. 注册用户
        print("1. 注册测试用户...")
        response = session.post(f"{BASE_URL}/api/users/register", json=test_user)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 用户注册成功")
        else:
            print(f"   ❌ 用户注册失败: {response.text}")
            return
        
        # 2. 登录获取token
        print("\n2. 用户登录...")
        response = session.post(f"{BASE_URL}/api/users/login", json=test_user)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            session.headers.update({"Authorization": f"Bearer {token}"})
            print("   ✅ 登录成功，获取到token")
        else:
            print(f"   ❌ 登录失败: {response.text}")
            return
        
        # 3. 测试用户信息更新 API
        print("\n3. 测试用户信息更新 API (PUT /api/users/me)...")
        response = session.put(f"{BASE_URL}/api/users/me", json=test_user_update)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            updated_user = response.json()
            # 更新token（因为用户名可能已更改）
            if "access_token" in updated_user:
                token = updated_user["access_token"]
                session.headers.update({"Authorization": f"Bearer {token}"})
            print(f"   ✅ 用户信息更新成功: {updated_user['username']}")
        else:
            print(f"   ❌ 用户信息更新失败: {response.text}")
        
        # 4. 创建会话用于后续测试
        print("\n4. 创建测试会话...")
        response = session.post(f"{BASE_URL}/api/conversations/", json={"title": "测试会话"})
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            conv_data = response.json()
            conversation_id = conv_data["id"]
            print(f"   ✅ 会话创建成功，ID: {conversation_id}")
        else:
            print(f"   ❌ 会话创建失败: {response.text}")
            return
        
        # 5. 测试会话标题更新 API
        print("\n5. 测试会话标题更新 API (PUT /api/conversations/{id})...")
        update_data = {"title": "更新后的会话标题"}
        response = session.put(f"{BASE_URL}/api/conversations/{conversation_id}", json=update_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            updated_conv = response.json()
            print(f"   ✅ 会话标题更新成功: {updated_conv['title']}")
        else:
            print(f"   ❌ 会话标题更新失败: {response.text}")
        
        # 6. 创建消息用于测试
        print("\n6. 创建测试消息...")
        message_data = {
            "content": "这是一条测试消息",
            "conversation_id": conversation_id,
            "enable_search": False,
            "enable_thinking": False
        }
        response = session.post(f"{BASE_URL}/api/messages/send", json=message_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 消息发送成功")
        else:
            print(f"   ❌ 消息发送失败: {response.text}")
        
        # 7. 获取消息列表
        print("\n7. 获取消息列表...")
        response = session.get(f"{BASE_URL}/api/messages/conversation/{conversation_id}")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            messages = response.json()
            if messages['messages']:
                message_id = messages['messages'][0]['id']
                print(f"   ✅ 获取到消息，ID: {message_id}")
            else:
                print("   ⚠️ 消息列表为空")
        else:
            print(f"   ❌ 获取消息失败: {response.text}")
        
        # 8. 测试消息内容更新 API
        if message_id:
            print("\n8. 测试消息内容更新 API (PUT /api/messages/{id})...")
            update_data = {"content": "这是更新后的消息内容"}
            response = session.put(f"{BASE_URL}/api/messages/{message_id}", json=update_data)
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                updated_msg = response.json()
                print(f"   ✅ 消息内容更新成功: {updated_msg['content']}")
            else:
                print(f"   ❌ 消息内容更新失败: {response.text}")
        
        # 9. 测试用户账户删除 API
        print("\n9. 测试用户账户删除 API (DELETE /api/users/me)...")
        response = session.delete(f"{BASE_URL}/api/users/me")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 用户账户删除成功")
        else:
            print(f"   ❌ 用户账户删除失败: {response.text}")
        
        print("\n" + "=" * 60)
        print("🏁 新增API测试完成！")
        print("\n测试的4个新增API:")
        print("✅ PUT /api/users/me - 更新用户信息")
        print("✅ PUT /api/conversations/{id} - 更新会话标题") 
        print("✅ PUT /api/messages/{id} - 更新消息内容")
        print("✅ DELETE /api/users/me - 删除用户账户")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {e}")

if __name__ == "__main__":
    print("新增CRUD API测试工具")
    print("确保后端服务已启动在 http://localhost:8000")
    print("按回车键开始测试...")
    input()
    test_new_apis()
