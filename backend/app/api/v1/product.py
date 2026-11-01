"""产品服务路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import db_session
from schemas.product import ProductInfo, ProductCreate, ProductUpdate
from services import product_service

router = APIRouter(prefix="/products", tags=["产品服务"])


@router.get("", response_model=list[ProductInfo], summary="获取产品列表")
def get_products(category: str | None = None, db: Session = db_session()):
    return product_service.get_products(db, category)


@router.get("/{product_id}", response_model=ProductInfo, summary="获取产品详情")
def get_product_detail(product_id: int, db: Session = db_session()):
    product = product_service.get_product_detail(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


@router.post("", response_model=ProductInfo, summary="新增产品")
def create_product(data: ProductCreate, db: Session = db_session()):
    return product_service.create_product(db, data)


@router.put("/{product_id}", response_model=ProductInfo, summary="更新产品")
def update_product(product_id: int, data: ProductUpdate, db: Session = db_session()):
    product = product_service.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


@router.delete("/{product_id}", summary="删除产品")
def delete_product(product_id: int, db: Session = db_session()):
    if not product_service.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="产品不存在")
    return {"message": "删除成功"}
