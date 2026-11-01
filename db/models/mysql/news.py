"""新闻动态模型"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.core.mysql_db import Base


class News(Base):
    """新闻动态表"""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="新闻标题")
    summary = Column(String(500), comment="新闻摘要")
    content = Column(Text, comment="新闻正文(HTML)")
    cover_url = Column(String(500), comment="封面图地址")
    category = Column(String(50), nullable=False, comment="新闻分类")
    author = Column(String(50), default="管理员", comment="作者")
    published_at = Column(DateTime, comment="发布时间")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
