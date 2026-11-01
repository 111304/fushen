"""新闻动态 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    summary: str = ""
    content: str = ""
    cover_url: str = ""
    category: str
    author: str = "管理员"
    published_at: datetime | None = None


class NewsCreate(NewsBase):
    """创建新闻模型"""
    pass


class NewsUpdate(BaseModel):
    """更新新闻模型（所有字段可选）"""

    title: str | None = None
    summary: str | None = None
    content: str | None = None
    cover_url: str | None = None
    category: str | None = None
    author: str | None = None
    published_at: datetime | None = None


class NewsInfo(BaseModel):
    """新闻响应模型"""

    id: int
    title: str
    summary: str
    content: str
    cover_url: str
    category: str
    author: str
    published_at: str

    class Config:
        from_attributes = True


class PageResult(BaseModel):
    """分页响应模型"""

    list: list[NewsInfo]
    total: int
    page: int
    page_size: int
