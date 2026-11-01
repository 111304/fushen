"""产品服务业务逻辑 - 含 Redis 缓存"""

import json
from sqlalchemy.orm import Session

from db.core.redis_client import redis_client
from db.models.mysql.product import Product
from schemas.product import ProductInfo, ProductCreate, ProductUpdate

CACHE_KEY_PRODUCTS = "products:list"
CACHE_KEY_PRODUCT_DETAIL = "product:detail:{id}"


def _parse_features(features_str: str | None) -> list[str]:
    """将数据库中 JSON 字符串解析为列表"""
    if not features_str:
        return []
    try:
        return json.loads(features_str)
    except (json.JSONDecodeError, TypeError):
        return []


def _to_info(product: Product) -> ProductInfo:
    """ORM 对象转响应模型"""
    return ProductInfo(
        id=product.id,
        name=product.name,
        description=product.description,
        image_url=product.image_url or "",
        category=product.category,
        features=_parse_features(product.features),
        sort_order=product.sort_order,
    )


def get_products(db: Session, category: str | None = None) -> list[ProductInfo]:
    """获取产品列表（优先读缓存）"""
    cache_key = f"{CACHE_KEY_PRODUCTS}:{category or 'all'}"
    cached = redis_client.get_json(cache_key)
    if cached:
        return [ProductInfo(**item) for item in cached]

    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    products = query.order_by(Product.sort_order).all()

    result = [_to_info(p) for p in products]
    redis_client.set_json(cache_key, [r.model_dump() for r in result])
    return result


def get_product_detail(db: Session, product_id: int) -> ProductInfo | None:
    """获取产品详情"""
    cache_key = CACHE_KEY_PRODUCT_DETAIL.format(id=product_id)
    cached = redis_client.get_json(cache_key)
    if cached:
        return ProductInfo(**cached)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    info = _to_info(product)
    redis_client.set_json(cache_key, info.model_dump())
    return info


def create_product(db: Session, data: ProductCreate) -> ProductInfo:
    """新增产品"""
    product = Product(
        name=data.name,
        description=data.description,
        image_url=data.image_url,
        category=data.category,
        features=json.dumps(data.features, ensure_ascii=False),
        sort_order=data.sort_order,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    _invalidate_cache()
    return _to_info(product)


def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductInfo | None:
    """更新产品"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    update_data = data.model_dump(exclude_unset=True)
    if "features" in update_data and update_data["features"] is not None:
        update_data["features"] = json.dumps(update_data["features"], ensure_ascii=False)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    _invalidate_cache()
    return _to_info(product)


def delete_product(db: Session, product_id: int) -> bool:
    """删除产品"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False

    db.delete(product)
    db.commit()
    _invalidate_cache()
    return True


def _invalidate_cache():
    """清除产品相关缓存"""
    for pattern_key in [CACHE_KEY_PRODUCTS, CACHE_KEY_PRODUCT_DETAIL]:
        redis_client.delete(pattern_key)
