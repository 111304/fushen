"""MongoDB 连接 (Motor 异步驱动)"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from db.config import settings

# MongoDB 异步客户端
mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_url)


def get_mongo_db() -> AsyncIOMotorDatabase:
    """获取 MongoDB 数据库实例"""
    return mongo_client[settings.mongo_database]
