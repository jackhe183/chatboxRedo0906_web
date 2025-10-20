数据存储使用mysql，存储如用户的历史数据和用户管理系统，
本地的mysql是：name：root，主机localhost，端口3306，用户名root，密码305857


1. 用户表 (users)
这个表用于存储用户的基本登录信息。

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


2. 会话表 (conversations)
该表用于组织每一次独立的对话。每个用户可以有多个会话。

CREATE TABLE conversations (
id SERIAL PRIMARY KEY,
user_id INTEGER NOT NULL,
title VARCHAR(255) NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fk_user
FOREIGN KEY(user_id)
REFERENCES users(id)
ON DELETE CASCADE -- 如果用户被删除，其所有会话也一并删除
);

3. 消息表 (`messages`)

此表核心用于存储用户与AI之间的每一轮问答。

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'user' for user's question, 'assistant' for model's answer
    content TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'completed', -- Can be 'processing', 'completed', 'failed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversation
        FOREIGN KEY(conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE -- 如果会话被删除，其所有消息也一并删除
);

关系图
[users] 1--* [conversations] 1--* [messages]
  |              |              |
  - id           - id           - id
  - username     - user_id      - conversation_id
  - ...          - title        - role
                 - ...          - content
                                - ...

工作流程与表如何协同
用户登录：在 users 表中验证 username 和 hashed_password。
开始新对话：
用户发送第一条消息 (e.g., "你好")。
后端首先在 conversations 表中创建一条新记录，title 此时可以是一个临时值（如 "新对话"）。
同时，在 messages 表中插入用户的第一条消息，role 为 'user'。
后端将用户的消息发送给大模型，同时在 messages 表中创建一条 role 为 'assistant' 且 status 为 'processing' 的记录。
大模型返回完整回答后，后端更新这条 'assistant' 消息的 content 和 status。
同时，后端调用大模型，根据第一轮问答内容生成一个会话标题 (e.g., "问候与介绍")，并更新 conversations 表中对应记录的 title 字段。
继续对话：
用户在当前会话中继续提问。
后端只需在 messages 表中为该 conversation_id 继续添加新的问答记录。
每次有新消息时，都更新 conversations 表的 updated_at 字段，便于排序。
加载历史会话：
后端根据 user_id 从 conversations 表中查询该用户的所有会话，并按 updated_at 降序排列后展示给前端。
用户点击某个会话标题。
前端传递对应的 conversation_id 给后端。
后端从 messages 表中查询所有 conversation_id 匹配的记录，并按 created_at 升序排列，返回给前端进行渲染，从而恢复历史对话。
