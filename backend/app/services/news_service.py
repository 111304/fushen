"""新闻动态业务逻辑 - 含 Redis 缓存"""

from sqlalchemy.orm import Session
from sqlalchemy import desc

from db.core.redis_client import redis_client
from db.models.mysql.news import News
from schemas.news import NewsInfo, NewsCreate, NewsUpdate, PageResult

CACHE_KEY_NEWS_LIST = "news:list:{category}:{page}:{size}"
CACHE_KEY_NEWS_DETAIL = "news:detail:{id}"


def _to_info(news: News) -> NewsInfo:
    """ORM 对象转响应模型"""
    return NewsInfo(
        id=news.id,
        title=news.title,
        summary=news.summary or "",
        content=news.content or "",
        cover_url=news.cover_url or "",
        category=news.category,
        author=news.author,
        published_at=news.published_at.strftime("%Y-%m-%d") if news.published_at else "",
    )


def get_news_list(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    category: str | None = None,
) -> PageResult:
    """获取新闻列表（分页，优先读缓存）"""
    cache_key = CACHE_KEY_NEWS_LIST.format(
        category=category or "all", page=page, size=page_size
    )
    cached = redis_client.get_json(cache_key)
    if cached:
        return PageResult(**cached)

    query = db.query(News)
    if category:
        query = query.filter(News.category == category)

    total = query.count()
    offset = (page - 1) * page_size
    news_list = (
        query.order_by(desc(News.published_at), desc(News.id))
        .offset(offset)
        .limit(page_size)
        .all()
    )

    result = PageResult(
        list=[_to_info(n) for n in news_list],
        total=total,
        page=page,
        page_size=page_size,
    )

    redis_client.set_json(cache_key, result.model_dump())
    return result


def get_news_detail(db: Session, news_id: int) -> NewsInfo | None:
    """获取新闻详情"""
    cache_key = CACHE_KEY_NEWS_DETAIL.format(id=news_id)
    cached = redis_client.get_json(cache_key)
    if cached:
        return NewsInfo(**cached)

    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return None

    info = _to_info(news)
    redis_client.set_json(cache_key, info.model_dump())
    return info


def create_news(db: Session, data: NewsCreate) -> NewsInfo:
    """新增新闻"""
    news = News(**data.model_dump())
    db.add(news)
    db.commit()
    db.refresh(news)

    _invalidate_cache()
    return _to_info(news)


def update_news(db: Session, news_id: int, data: NewsUpdate) -> NewsInfo | None:
    """更新新闻"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(news, field, value)

    db.commit()
    db.refresh(news)

    _invalidate_cache(news_id)
    return _to_info(news)


def delete_news(db: Session, news_id: int) -> bool:
    """删除新闻"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return False

    db.delete(news)
    db.commit()
    _invalidate_cache(news_id)
    return True


def _invalidate_cache(news_id: int | None = None) -> None:
    """清除新闻相关缓存

    列表缓存键含分类/页码/条数（news:list:all:1:10 等），明细键含真实 id，
    模板常量本身不是真实键，必须按前缀或格式化后的键清除。
    """
    redis_client.delete_pattern("news:list:*")
    if news_id is not None:
        redis_client.delete(CACHE_KEY_NEWS_DETAIL.format(id=news_id))
