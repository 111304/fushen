"""产品服务模型"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.core.mysql_db import Base


class Product(Base):
    """产品服务表"""

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="产品名称")
    description = Column(Text, nullable=False, comment="产品描述")
    image_url = Column(String(500), comment="产品图片地址")
    category = Column(String(50), nullable=False, comment="产品分类")
    features = Column(Text, comment="核心功能(JSON数组)")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
