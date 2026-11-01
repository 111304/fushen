"""公司信息业务逻辑 - 含 Redis 缓存"""

import json
from sqlalchemy.orm import Session

from db.core.redis_client import redis_client
from db.models.mysql.company import Company, TeamMember
from schemas.company import CompanyInfo, CompanyUpdate, TeamMemberInfo, TeamMemberCreate

CACHE_KEY_COMPANY = "company:info"
CACHE_KEY_TEAM = "company:team"


def get_company(db: Session) -> CompanyInfo:
    """获取公司信息（优先读缓存）"""
    cached = redis_client.get_json(CACHE_KEY_COMPANY)
    if cached:
        return CompanyInfo(**cached)

    company = db.query(Company).first()
    if not company:
        # 无数据时返回默认值
        return CompanyInfo(
            id=0,
            name="星辰科技",
            slogan="让AI驱动未来",
            description="星辰科技，专注于AI与云计算的高新技术企业。",
            logo_url="/favicon.svg",
            banner_url="https://picsum.photos/seed/stellar-hero/1920/600",
            about_image_url="https://picsum.photos/seed/stellar-about/600/400",
            address="北京市海淀区中关村科技园",
            phone="010-8888-6666",
            email="contact@stellartech.com",
            founded_year=2018,
        )

    info = CompanyInfo.model_validate(company)
    redis_client.set_json(CACHE_KEY_COMPANY, info.model_dump())
    return info


def update_company(db: Session, data: CompanyUpdate) -> CompanyInfo:
    """更新公司信息，同时刷新缓存"""
    company = db.query(Company).first()
    if not company:
        company = Company(name="星辰科技", slogan="让AI驱动未来", description="")
        db.add(company)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)

    info = CompanyInfo.model_validate(company)
    redis_client.set_json(CACHE_KEY_COMPANY, info.model_dump())
    return info


def get_team_members(db: Session) -> list[TeamMemberInfo]:
    """获取团队成员列表（优先读缓存）"""
    cached = redis_client.get_json(CACHE_KEY_TEAM)
    if cached:
        return [TeamMemberInfo(**item) for item in cached]

    members = db.query(TeamMember).order_by(TeamMember.sort_order).all()
    result = [TeamMemberInfo.model_validate(m) for m in members]

    if result:
        redis_client.set_json(CACHE_KEY_TEAM, [r.model_dump() for r in result])

    return result


def create_team_member(db: Session, data: TeamMemberCreate) -> TeamMemberInfo:
    """新增团队成员"""
    member = TeamMember(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)

    redis_client.delete(CACHE_KEY_TEAM)
    return TeamMemberInfo.model_validate(member)
