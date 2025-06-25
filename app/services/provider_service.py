from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.provider_model import ProviderBase, ProviderCreate, ProviderUpdate

class ProviderService:
    @staticmethod
    async def create_provider(data: ProviderCreate):
        collection = db["providers"]
        now = datetime.utcnow()
        new_data = data.dict()
        new_data.update({"created_at": now, "updated_at": now})
        result = await collection.insert_one(new_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_providers():
        collection = db["providers"]
        cursor = collection.find()
        providers = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            providers.append(ProviderBase(**doc))
        return providers

    @staticmethod
    async def update_provider(data: ProviderUpdate):
        collection = db["providers"]
        update_data = data.dict()
        update_data.pop("id")
        update_data["updated_at"] = datetime.utcnow()
        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        return {"status": "success" if result.modified_count else "not updated"}

    @staticmethod
    async def delete_provider(id: str):
        collection = db["providers"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        return {"status": "success" if result.deleted_count else "not deleted"}
