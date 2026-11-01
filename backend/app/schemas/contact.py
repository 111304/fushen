"""联系表单 Pydantic 模型"""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    """提交联系表单模型"""

    name: str
    email: EmailStr
    phone: str = ""
    subject: str
    message: str


class ContactInfo(BaseModel):
    """联系消息响应模型（用于管理后台查看）"""

    id: str
    name: str
    email: str
    phone: str
    subject: str
    message: str
    status: str = "pending"
    created_at: str

    class Config:
        from_attributes = True
