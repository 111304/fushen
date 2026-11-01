"""公司信息 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel


class CompanyInfo(BaseModel):
    """公司信息响应模型"""

    id: int
    name: str
    slogan: str
    description: str
    logo_url: str
    banner_url: str
    about_image_url: str
    address: str
    phone: str
    email: str
    founded_year: int

    class Config:
        from_attributes = True


class CompanyUpdate(BaseModel):
    """公司信息更新模型（所有字段可选）"""

    name: str | None = None
    slogan: str | None = None
    description: str | None = None
    logo_url: str | None = None
    banner_url: str | None = None
    about_image_url: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    founded_year: int | None = None


class TeamMemberInfo(BaseModel):
    """团队成员响应模型"""

    id: int
    name: str
    title: str
    avatar_url: str
    bio: str

    class Config:
        from_attributes = True


class TeamMemberCreate(BaseModel):
    """创建团队成员模型"""

    name: str
    title: str
    avatar_url: str = ""
    bio: str = ""
    sort_order: int = 0
