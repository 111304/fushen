"""应用配置 - 从 backend/.env 读取环境变量

注意：数据库相关配置（MySQL/Redis/MongoDB）已迁移到同级 db 包的 `db/config.py`
与 `db/.env`，本文件仅保留应用级配置（标题、版本、CORS）。
"""

from pathlib import Path

from pydantic_settings import BaseSettings

# backend 目录（应用 .env 位于 backend/ 下）
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # App
    app_title: str = "星辰科技公司网站API"
    app_version: str = "1.0.0"
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
