from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.middlewares.cors import setup_cors
from app.core.init_data import init_data
from app.services.permission_scanner import sync_permissions
from app.core.logger import logger


# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化数据
db = SessionLocal()
try:
    init_data(db)
except Exception as e:
    print(f"初始化数据时发生错误: {e}")
finally:
    db.close()


app = FastAPI(
    title=settings.app["name"],
    version=settings.app["version"],
    debug=settings.app["debug"]
)

# 设置CORS中间件
setup_cors(app)

# 注册API路由
app.include_router(api_router)

# 同步权限
logger.info("开始同步权限...")
db = SessionLocal()
try:
    created_count = sync_permissions(app, db)
    logger.info(f"权限同步完成，创建了 {created_count} 个新权限")
except Exception as e:
    logger.error(f"同步权限时发生错误: {e}")
finally:
    db.close()
logger.info("权限同步流程结束")


@app.get("/")
def read_root():
    """根路径"""
    return {"message": "Welcome to Permission Management System API"}


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}
