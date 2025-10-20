from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from database.models import MessageRole, MessageStatus
from pydantic import Field

# 用户相关
class UserCreate(BaseModel):
    username: str
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v or len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度必须在3-20个字符之间')
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('密码长度至少6个字符')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if v is not None:
            if not v or len(v) < 3 or len(v) > 20:
                raise ValueError('用户名长度必须在3-20个字符之间')
            if not v.replace('_', '').isalnum():
                raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if v is not None and (not v or len(v) < 6):
            raise ValueError('密码长度至少6个字符')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str

# 会话相关
class ConversationCreate(BaseModel):
    title: Optional[str] = "新对话"

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]

class ConversationUpdate(BaseModel):
    title: str
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('会话标题不能为空')
        if len(v) > 100:
            raise ValueError('会话标题不能超过100个字符')
        return v.strip()

# 消息相关
class MessageCreate(BaseModel):
    content: str
    conversation_id: Optional[int] = None
    enable_search: Optional[bool] = False
    enable_thinking: Optional[bool] = False
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('消息内容不能为空')
        if len(v) > 10000:
            raise ValueError('消息内容不能超过10000个字符')
        return v.strip()

class MessageResponse(BaseModel):
    id: int
    role: MessageRole
    content: str
    status: MessageStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageListResponse(BaseModel):
    messages: List[MessageResponse]

class MessageUpdate(BaseModel):
    content: str
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('消息内容不能为空')
        if len(v) > 10000:
            raise ValueError('消息内容不能超过10000个字符')
        return v.strip()

# 流式响应
class StreamChunk(BaseModel):
    type: str  # "content", "thinking", "done", "error", "conversation", "message"
    content: Optional[str] = None
    conversation_id: Optional[int] = None
    message_id: Optional[int] = None


class LLMHistoryItem(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str