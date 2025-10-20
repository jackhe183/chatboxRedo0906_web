from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "mysql+pymysql://root:305857@localhost:3306/chatbox"
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "305857"
    db_name: str = "chatbox"
    
    # JWT配置
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM配置
    siliconflow_api_key: str = "sk-xjfkcbhkqyognkrgsgldlgcboubdululbrzzflvnxglofmfg"
    siliconflow_base_url: str = "https://api.siliconflow.cn/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
