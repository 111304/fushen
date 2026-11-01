"""星辰科技公司网站 - FastAPI 主入口"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.core.mysql_db import Base, engine
from api.v1 import company, product, news, contact


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建 MySQL 表"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
api_prefix = "/api"
app.include_router(company.router, prefix=api_prefix)
app.include_router(product.router, prefix=api_prefix)
app.include_router(news.router, prefix=api_prefix)
app.include_router(contact.router, prefix=api_prefix)


@app.get("/", tags=["健康检查"])
def health_check():
    return {"status": "ok", "service": settings.app_title, "version": settings.app_version}
