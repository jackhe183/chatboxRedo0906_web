"""
启动脚本
"""
import uvicorn
from app import app

if __name__ == "__main__":
    print("🚀 启动 ChatBox 后端服务...")
    print("📖 API文档地址: http://localhost:8000/docs")
    print("🔧 健康检查: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
