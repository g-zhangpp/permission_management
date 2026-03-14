import os
import logging
from logging.handlers import RotatingFileHandler
from app.core.config import settings


class SQLAlchemyFilter(logging.Filter):
    def filter(self, record):
        # 过滤掉SQLAlchemy的日志
        return not record.name.startswith('sqlalchemy')


class Logger:
    def __init__(self):
        self.log_dir = settings.logger.get("log_dir", "./logs")
        self.log_file = settings.logger.get("log_file", "app.log")
        self.debug = settings.logger.get("debug", True)
        self.logger = None
        self.setup_logger()
    
    def setup_logger(self):
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 构建日志文件路径
        log_file_path = os.path.join(self.log_dir, self.log_file)
        
        # 创建logger
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # 清除已有的处理器
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        
        # 创建文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5  # 保留5个备份
        )
        file_handler.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加过滤器
        sqlalchemy_filter = SQLAlchemyFilter()
        file_handler.addFilter(sqlalchemy_filter)
        console_handler.addFilter(sqlalchemy_filter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger


# 创建全局日志对象
logger = Logger().get_logger()
