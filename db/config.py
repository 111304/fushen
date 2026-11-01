"""数据库配置 - MySQL / Redis / MongoDB 连接参数

从本包同级的 db/.env 读取数据库环境变量，也可由容器环境变量直接覆盖。
本配置独立于后端应用配置，供 db 包内连接层使用。
"""

from pathlib import Path

from pydantic_settings import BaseSettings

# db 包所在目录（数据库 .env 物理上随 db 包存放）
BASE_DIR = Path(__file__).resolve().parent


class DBSettings(BaseSettings):
    # MySQL
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = "stellar_tech"

    # Redis
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    # MongoDB
    mongo_host: str = "127.0.0.1"
    mongo_port: int = 27017
    mongo_user: str = ""
    mongo_password: str = ""
    mongo_database: str = "stellar_tech"

    # 缓存 TTL（Redis 相关）
    cache_ttl: int = 3600

    @property
    def mysql_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )

    @property
    def redis_url(self) -> str:
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def mongo_url(self) -> str:
        if self.mongo_user:
            return (
                f"mongodb://{self.mongo_user}:{self.mongo_password}"
                f"@{self.mongo_host}:{self.mongo_port}"
            )
        return f"mongodb://{self.mongo_host}:{self.mongo_port}"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"


settings = DBSettings()
