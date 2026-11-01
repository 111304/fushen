"""FastAPI 依赖注入"""

from fastapi import Depends
from sqlalchemy.orm import Session

from db.core.mysql_db import get_db
from db.core.mongo_db import get_mongo_db
from motor.motor_asyncio import AsyncIOMotorDatabase


def db_session() -> Session:
    """MySQL 数据库会话依赖"""
    return Depends(get_db)


def mongo_db() -> AsyncIOMotorDatabase:
    """MongoDB 数据库依赖"""
    return get_mongo_db()
