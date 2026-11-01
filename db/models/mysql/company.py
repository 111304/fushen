"""公司信息 & 团队成员模型"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.core.mysql_db import Base


class Company(Base):
    """公司信息表"""

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="公司名称")
    slogan = Column(String(200), nullable=False, comment="公司标语")
    description = Column(Text, nullable=False, comment="公司简介")
    logo_url = Column(String(500), default="/favicon.svg", comment="Logo地址")
    banner_url = Column(String(500), comment="首页横幅图地址")
    about_image_url = Column(String(500), comment="关于我们图片地址")
    address = Column(String(300), comment="公司地址")
    phone = Column(String(50), comment="联系电话")
    email = Column(String(100), comment="企业邮箱")
    founded_year = Column(Integer, comment="成立年份")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TeamMember(Base):
    """团队成员表"""

    __tablename__ = "team_member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="姓名")
    title = Column(String(100), nullable=False, comment="职位")
    avatar_url = Column(String(500), comment="头像地址")
    bio = Column(Text, comment="个人简介")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.utcnow)
