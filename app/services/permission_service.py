from app.db.mongo import db
from datetime import datetime
from bson import ObjectId
from app.models.permission_model import PermissionCreate, PermissionUpdate, PermissionBase

class PermissionService:
    @staticmethod
    async def create_permission(data: PermissionCreate):
        collection = db["permissions"]

        existing = await collection.find_one({"slug": data.slug})
        if existing:
            return {"status": "Permission already exists"}

        now = datetime.utcnow()
        permission = {
            "name": data.name,
            "slug": data.slug,
            "type": data.type,
            "created_at": now,
            "updated_at": now,
        }

        result = await collection.insert_one(permission)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_permissions():
        collection = db["permissions"]
        cursor = collection.find()
        result = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            result.append(PermissionBase(**doc))
        return result

    @staticmethod
    async def update_permission(data: PermissionUpdate):
        collection = db["permissions"]
        update_data = {
            "name": data.name,
            "slug": data.slug,
            "type": data.type,
            "updated_at": datetime.utcnow()
        }
        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete_permission(id: str):
        collection = db["permissions"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
