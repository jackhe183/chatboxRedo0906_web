#!/usr/bin/env python3
"""
快速测试脚本 - 验证token更新修复
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def quick_test():
    """快速测试token更新修复"""
    
    test_user = {
        "username": "quicktest",
        "password": "quickpass123"
    }
    
    test_user_update = {
        "username": "quicktestupdated",
        "password": "quickpass456"
    }
    
    session = requests.Session()
    
    print("🚀 快速测试token更新修复")
    print("=" * 40)
    
    try:
        # 1. 注册用户
        print("1. 注册用户...")
        response = session.post(f"{BASE_URL}/api/users/register", json=test_user)
        print(f"   状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ 注册失败: {response.text}")
            return
        
        # 2. 登录
        print("2. 用户登录...")
        response = session.post(f"{BASE_URL}/api/users/login", json=test_user)
        print(f"   状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ 登录失败: {response.text}")
            return
        
        token_data = response.json()
        token = token_data["access_token"]
        session.headers.update({"Authorization": f"Bearer {token}"})
        print("   ✅ 登录成功")
        
        # 3. 更新用户信息
        print("3. 更新用户信息...")
        response = session.put(f"{BASE_URL}/api/users/me", json=test_user_update)
        print(f"   状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ 更新失败: {response.text}")
            return
        
        updated_user = response.json()
        print(f"   ✅ 更新成功: {updated_user['username']}")
        
        # 4. 检查是否返回了新token
        if "access_token" in updated_user:
            new_token = updated_user["access_token"]
            session.headers.update({"Authorization": f"Bearer {new_token}"})
            print("   ✅ 获取到新token")
        else:
            print("   ⚠️ 未返回新token")
        
        # 5. 测试后续API调用
        print("4. 测试后续API调用...")
        response = session.post(f"{BASE_URL}/api/conversations/", json={"title": "测试会话"})
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 后续API调用成功")
        else:
            print(f"   ❌ 后续API调用失败: {response.text}")
        
        # 6. 清理
        print("5. 清理测试数据...")
        response = session.delete(f"{BASE_URL}/api/users/me")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 清理完成")
        else:
            print(f"   ⚠️ 清理失败: {response.text}")
        
        print("\n" + "=" * 40)
        print("🏁 快速测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {e}")

if __name__ == "__main__":
    quick_test()
