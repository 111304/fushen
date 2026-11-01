"""新闻动态路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import db_session
from schemas.news import NewsInfo, NewsCreate, NewsUpdate, PageResult
from services import news_service

router = APIRouter(prefix="/news", tags=["新闻动态"])


@router.get("", response_model=PageResult, summary="获取新闻列表(分页)")
def get_news_list(
    page: int = 1,
    page_size: int = 10,
    category: str | None = None,
    db: Session = db_session(),
):
    return news_service.get_news_list(db, page, page_size, category)


@router.get("/{news_id}", response_model=NewsInfo, summary="获取新闻详情")
def get_news_detail(news_id: int, db: Session = db_session()):
    news = news_service.get_news_detail(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return news


@router.post("", response_model=NewsInfo, summary="新增新闻")
def create_news(data: NewsCreate, db: Session = db_session()):
    return news_service.create_news(db, data)


@router.put("/{news_id}", response_model=NewsInfo, summary="更新新闻")
def update_news(news_id: int, data: NewsUpdate, db: Session = db_session()):
    news = news_service.update_news(db, news_id, data)
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    return news


@router.delete("/{news_id}", summary="删除新闻")
def delete_news(news_id: int, db: Session = db_session()):
    if not news_service.delete_news(db, news_id):
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {"message": "删除成功"}
