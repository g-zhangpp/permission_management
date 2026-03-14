import yaml
from pydantic_settings import BaseSettings
from typing import List, Dict, Any


class Settings(BaseSettings):
    app: Dict[str, Any]
    server: Dict[str, Any]
    database: Dict[str, Any]
    redis: Dict[str, Any]
    jwt: Dict[str, Any]
    cors: Dict[str, Any]
    init_data: Dict[str, Any] = {}

    class Config:
        env_file = ".env"
        extra = "allow"


def load_config() -> Settings:
    with open("app/core/config.yaml", "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    return Settings(**config_data)


settings = load_config()
