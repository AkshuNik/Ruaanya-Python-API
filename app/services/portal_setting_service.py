from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.portal_setting_model import PortalSettingCreate, PortalSettingUpdate, PortalSettingBase

class PortalSettingService:
    @staticmethod
    async def create(data: PortalSettingCreate):
        collection = db["portal_settings"]
        now = datetime.utcnow()
        new_data = data.dict()
        new_data.update({"created_at": now, "updated_at": now})
        result = await collection.insert_one(new_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def list_all():
        collection = db["portal_settings"]
        cursor = collection.find()
        settings = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            settings.append(PortalSettingBase(**doc))
        return settings

    @staticmethod
    async def update(data: PortalSettingUpdate):
        collection = db["portal_settings"]
        update_data = data.dict()
        update_data.pop("id")
        update_data["updated_at"] = datetime.utcnow()
        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete(id: str):
        collection = db["portal_settings"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
