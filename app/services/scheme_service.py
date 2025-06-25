from app.db.mongo import db
from datetime import datetime
from bson import ObjectId
from app.models.scheme_model import SchemeCreate, SchemeUpdate, SchemeBase

class SchemeService:
    @staticmethod
    async def create_scheme(data: SchemeCreate):
        collection = db["schemes"]
        now = datetime.utcnow()

        scheme = {
            "name": data.name,
            "status": data.status,
            "created_at": now,
            "updated_at": now
        }

        result = await collection.insert_one(scheme)
        return {"status": "success", "id": str(result.inserted_id)}

    # @staticmethod
    # async def get_schemes():
    #     collection = db["schemes"]
    #     cursor = collection.find()
    #     schemes = []
    #     async for doc in cursor:
    #         doc["id"] = str(doc["_id"])
    #         schemes.append(SchemeBase(**doc))
    #     return schemes
    
    @staticmethod
    async def get_schemes(status: str = None):
        collection = db["schemes"]

        query = {}
        if status:
            query["status"] = status  # Only filter if status is provided

        cursor = collection.find(query)
        schemes = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            schemes.append(SchemeBase(**doc))
        return schemes


    @staticmethod
    async def update_scheme(data: SchemeUpdate):
        collection = db["schemes"]
        update_data = {
            "name": data.name,
            "status": data.status,
            "updated_at": datetime.utcnow()
        }
        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    # @staticmethod
    async def delete_scheme(id: str):
        collection = db["schemes"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}

    # @staticmethod
    # async def delete_scheme(id: str):
    # scheme_collection = db["schemes"]
    # commission_collection = db["commissions"]

    # scheme_obj_id = ObjectId(id)
    # scheme_result = await scheme_collection.delete_one({"_id": scheme_obj_id})

    # if scheme_result.deleted_count:
    #     await commission_collection.delete_many({"scheme_id": id})
    #     return {"status": "success", "message": "Scheme and related commissions deleted."}
    
    # return {"status": "failed", "message": "Scheme not found"}
