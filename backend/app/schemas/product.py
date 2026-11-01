"""产品服务 Pydantic 模型"""

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    image_url: str = ""
    category: str
    features: list[str] = []
    sort_order: int = 0


class ProductCreate(ProductBase):
    """创建产品模型"""
    pass


class ProductUpdate(BaseModel):
    """更新产品模型（所有字段可选）"""

    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    category: str | None = None
    features: list[str] | None = None
    sort_order: int | None = None


class ProductInfo(BaseModel):
    """产品响应模型"""

    id: int
    name: str
    description: str
    image_url: str
    category: str
    features: list[str]
    sort_order: int

    class Config:
        from_attributes = True
