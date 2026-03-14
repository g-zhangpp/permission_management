from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def setup_cors(app):
    """设置CORS中间件"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors["origins"],
        allow_credentials=settings.cors["credentials"],
        allow_methods=settings.cors["methods"],
        allow_headers=settings.cors["headers"],
    )
