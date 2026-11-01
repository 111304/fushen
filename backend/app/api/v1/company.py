"""公司信息路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import db_session
from schemas.company import CompanyInfo, CompanyUpdate, TeamMemberInfo, TeamMemberCreate
from services import company_service

router = APIRouter(prefix="/company", tags=["公司信息"])


@router.get("/info", response_model=CompanyInfo, summary="获取公司信息")
def get_company_info(db: Session = db_session()):
    return company_service.get_company(db)


@router.put("/info", response_model=CompanyInfo, summary="更新公司信息")
def update_company_info(data: CompanyUpdate, db: Session = db_session()):
    return company_service.update_company(db, data)


@router.get("/team", response_model=list[TeamMemberInfo], summary="获取团队成员")
def get_team(db: Session = db_session()):
    return company_service.get_team_members(db)


@router.post("/team", response_model=TeamMemberInfo, summary="新增团队成员")
def create_team_member(data: TeamMemberCreate, db: Session = db_session()):
    return company_service.create_team_member(db, data)






