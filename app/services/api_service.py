from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.api_model import ApiCreate, ApiUpdate, ApiBase

class ApiService:
    @staticmethod
    async def create_api(data: ApiCreate):
        collection = db["apis"]
        now = datetime.utcnow()
        new_api = data.dict()
        new_api.update({"created_at": now, "updated_at": now})

        result = await collection.insert_one(new_api)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_apis():
        collection = db["apis"]
        cursor = collection.find()
        apis = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            apis.append(ApiBase(**doc))
        return apis

    @staticmethod
    async def update_api(data: ApiUpdate):
        collection = db["apis"]
        update_data = data.dict()
        update_data.pop("id")
        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete_api(id: str):
        collection = db["apis"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
