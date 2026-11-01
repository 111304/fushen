"""联系表单业务逻辑 - MongoDB 存储"""

from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.contact import ContactCreate, ContactInfo

COLLECTION_NAME = "contact_messages"


async def submit_contact(db: AsyncIOMotorDatabase, data: ContactCreate) -> str:
    """保存联系表单到 MongoDB"""
    document = {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "subject": data.subject,
        "message": data.message,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }
    result = await db[COLLECTION_NAME].insert_one(document)
    return str(result.inserted_id)


async def get_contact_list(
    db: AsyncIOMotorDatabase,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
) -> dict:
    """获取联系消息列表（管理后台用）"""
    query = {}
    if status:
        query["status"] = status

    total = await db[COLLECTION_NAME].count_documents(query)
    skip = (page - 1) * page_size
    cursor = db[COLLECTION_NAME].find(query).sort("created_at", -1).skip(skip).limit(page_size)
    docs = await cursor.to_list(length=page_size)

    items = [
        ContactInfo(
            id=str(doc["_id"]),
            name=doc["name"],
            email=doc["email"],
            phone=doc.get("phone", ""),
            subject=doc["subject"],
            message=doc["message"],
            status=doc.get("status", "pending"),
            created_at=doc.get("created_at", ""),
        )
        for doc in docs
    ]

    return {"list": [item.model_dump() for item in items], "total": total, "page": page, "page_size": page_size}


async def update_contact_status(
    db: AsyncIOMotorDatabase, message_id: str, status: str
) -> bool:
    """更新联系消息状态"""
    result = await db[COLLECTION_NAME].update_one(
        {"_id": ObjectId(message_id)},
        {"$set": {"status": status}},
    )
    return result.modified_count > 0
