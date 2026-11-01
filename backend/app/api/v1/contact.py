"""联系表单路由 - MongoDB 存储"""

from fastapi import APIRouter
from db.core.mongo_db import get_mongo_db
from schemas.contact import ContactCreate
from services import contact_service

router = APIRouter(prefix="/contact", tags=["联系我们"])


@router.post("", summary="提交联系表单")
async def submit_contact(data: ContactCreate):
    db = get_mongo_db()
    message_id = await contact_service.submit_contact(db, data)
    return {"code": 200, "message": "提交成功", "data": {"id": message_id}}


@router.get("", summary="获取联系消息列表(管理后台用)")
async def get_contact_list(page: int = 1, page_size: int = 20, status: str | None = None):
    db = get_mongo_db()
    result = await contact_service.get_contact_list(db, page, page_size, status)
    return {"code": 200, "message": "success", "data": result}


@router.put("/{message_id}/status", summary="更新消息状态")
async def update_contact_status(message_id: str, status: str):
    db = get_mongo_db()
    success = await contact_service.update_contact_status(db, message_id, status)
    if not success:
        return {"code": 404, "message": "消息不存在", "data": None}
    return {"code": 200, "message": "更新成功", "data": None}
