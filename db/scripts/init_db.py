"""数据库初始化脚本 - 创建表并写入种子数据

使用方式（在项目根目录执行，db 包已随项目位于根下）:
    cd <项目根目录>
    python -m db.scripts.init_db
"""

import json
from datetime import datetime

from db.core.mysql_db import engine, SessionLocal, Base
from db.models.mysql.company import Company, TeamMember
from db.models.mysql.product import Product
from db.models.mysql.news import News


def init_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)
    print("[1/4] MySQL 表创建完成")


def seed_company(db):
    """写入公司信息"""
    if db.query(Company).first():
        print("[2/4] 公司信息已存在，跳过")
        return

    company = Company(
        name="星辰科技",
        slogan="让AI驱动未来",
        description=(
            "星辰科技成立于2018年，是一家专注于人工智能与云计算的高新技术企业。"
            "我们致力于为企业提供从AI算法、云原生架构到数字化转型咨询的全链路解决方案，"
            "已服务超过500家企业客户。"
        ),
        logo_url="/favicon.svg",
        banner_url="https://picsum.photos/seed/stellar-hero/1920/600",
        about_image_url="https://picsum.photos/seed/stellar-about/600/400",
        address="北京市海淀区中关村科技园",
        phone="010-8888-6666",
        email="contact@stellartech.com",
        founded_year=2018,
    )
    db.add(company)
    db.commit()
    print("[2/4] 公司信息写入完成")


def seed_team(db):
    """写入团队成员"""
    if db.query(TeamMember).first():
        print("[3/4] 团队成员已存在，跳过")
        return

    members = [
        TeamMember(name="张明", title="CEO & 创始人",
                   avatar_url="https://picsum.photos/seed/team-1/200/200",
                   bio="清华大学计算机博士，曾任某头部互联网公司技术VP，15年AI领域经验。",
                   sort_order=1),
        TeamMember(name="李华", title="CTO",
                   avatar_url="https://picsum.photos/seed/team-2/200/200",
                   bio="前Google资深工程师，云原生架构专家，主导多个大型分布式系统设计。",
                   sort_order=2),
        TeamMember(name="王芳", title="产品VP",
                   avatar_url="https://picsum.photos/seed/team-3/200/200",
                   bio="10年企业级产品经验，擅长AI产品化与商业化落地。",
                   sort_order=3),
        TeamMember(name="赵强", title="数据科学家",
                   avatar_url="https://picsum.photos/seed/team-4/200/200",
                   bio="MIT统计学硕士，Kaggle Grandmaster，专注机器学习与大数据分析。",
                   sort_order=4),
    ]
    db.add_all(members)
    db.commit()
    print("[3/4] 团队成员写入完成")


def seed_products(db):
    """写入产品数据"""
    if db.query(Product).first():
        print("[4/4] 产品数据已存在，跳过")
        return

    products = [
        Product(name="星辰AI平台", category="AI平台",
                description="一站式AI模型训练与部署平台，支持从数据标注到模型上线的全流程管理。",
                image_url="https://picsum.photos/seed/product-1/400/300",
                features=json.dumps(["模型训练", "自动标注", "在线推理", "模型版本管理"]),
                sort_order=1),
        Product(name="云原生架构服务", category="云计算",
                description="基于Kubernetes的微服务架构设计与实施，助力企业应用现代化改造。",
                image_url="https://picsum.photos/seed/product-2/400/300",
                features=json.dumps(["微服务设计", "容器编排", "CI/CD流水线", "可观测性"]),
                sort_order=2),
        Product(name="智能数据分析", category="数据分析",
                description="基于大数据的实时分析平台，提供可视化看板与智能决策支持。",
                image_url="https://picsum.photos/seed/product-3/400/300",
                features=json.dumps(["实时计算", "可视化看板", "智能预警", "多维分析"]),
                sort_order=3),
        Product(name="数字化咨询", category="咨询服务",
                description="资深专家团队提供数字化转型战略规划与落地实施咨询服务。",
                image_url="https://picsum.photos/seed/product-4/400/300",
                features=json.dumps(["战略规划", "技术选型", "架构评审", "实施指导"]),
                sort_order=4),
    ]
    db.add_all(products)
    db.commit()
    print("[4/4] 产品数据写入完成")


def seed_news(db):
    """写入新闻数据"""
    if db.query(News).first():
        return

    news_list = [
        News(title="星辰科技完成B轮融资，加速AI产品研发",
             summary="本轮融资将用于加大AI核心技术研发投入，扩大市场份额。",
             content="<p>详细内容...</p>", category="公司动态",
             cover_url="https://picsum.photos/seed/news-1/400/250",
             author="市场部", published_at=datetime(2025, 7, 15)),
        News(title="星辰AI平台3.0版本正式发布",
             summary="全新版本支持大模型微调与多模态推理，性能提升200%。",
             content="<p>详细内容...</p>", category="产品发布",
             cover_url="https://picsum.photos/seed/news-2/400/250",
             author="产品部", published_at=datetime(2025, 6, 28)),
        News(title="与某头部企业签署战略合作协议",
             summary="双方将在AI+工业领域展开深度合作，共建智能工厂。",
             content="<p>详细内容...</p>", category="合作动态",
             cover_url="https://picsum.photos/seed/news-3/400/250",
             author="商务部", published_at=datetime(2025, 5, 10)),
    ]
    db.add_all(news_list)
    db.commit()
    print("    新闻数据写入完成")


def main():
    print("=" * 50)
    print("星辰科技 - 数据库初始化")
    print("=" * 50)

    init_tables()

    db = SessionLocal()
    try:
        seed_company(db)
        seed_team(db)
        seed_products(db)
        seed_news(db)
    finally:
        db.close()

    print("=" * 50)
    print("初始化完成！请访问 http://127.0.0.1:8000/docs 查看 API 文档")
    print("=" * 50)


if __name__ == "__main__":
    main()
