from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database.database import engine, Base
from routers import users, conversations, messages


# 创建数据库表
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时清理资源
    pass

# 创建FastAPI应用
app = FastAPI(
    title="ChatBox API",
    description="一个轻量级的仿ChatGPT聊天应用",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "ChatBox API 服务正在运行",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )