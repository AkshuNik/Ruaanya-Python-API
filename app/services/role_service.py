from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
import pytz
from app.models.role_model import RoleOut

IST = pytz.timezone("Asia/Kolkata")

class RoleService:
    @staticmethod
    async def create_role(data):
        role = {
            "name": data.name,
            "slug": data.slug,
            "created_at": datetime.now(IST),
            "updated_at": datetime.now(IST),
        }
        result = await db["roles"].insert_one(role)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_roles():
        roles = []
        cursor = db["roles"].find()
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            roles.append(RoleOut(**doc))
        return roles

    @staticmethod
    async def update_role(data):
        update_data = {
            "name": data.name,
            "slug": data.slug,
            "updated_at": datetime.now(IST),
        }
        result = await db["roles"].update_one(
            {"_id": ObjectId(data.id)}, {"$set": update_data}
        )
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not_modified"}

    @staticmethod
    async def delete_role(role_id: str):
        result = await db["roles"].delete_one({"_id": ObjectId(role_id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not_found"}
