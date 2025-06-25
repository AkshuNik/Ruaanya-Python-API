from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.commission_model import CommissionBase, CommissionCreate, CommissionUpdate

class CommissionService:
    @staticmethod
    async def create_commission(data: CommissionCreate):
        collection = db["commissions"]
        now = datetime.utcnow()
        new_data = data.dict()
        new_data.update({"created_at": now, "updated_at": now})
        result = await collection.insert_one(new_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_commissions():
        collection = db["commissions"]
        cursor = collection.find()
        commissions = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            commissions.append(CommissionBase(**doc))
        return commissions

    # @staticmethod
    # async def update_commission(data: CommissionUpdate):
    #     collection = db["commissions"]
    #     update_data = data.dict()
    #     update_data.pop("id")
    #     update_data["updated_at"] = datetime.utcnow()
    #     result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
    #     return {"status": "success" if result.modified_count else "not updated"}

    @staticmethod
    async def delete_commission(id: str):
        collection = db["commissions"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        return {"status": "success" if result.deleted_count else "not deleted"}

    @staticmethod
    async def update_commission_by_id_and_scheme(id: str, scheme_id: str, data: dict):
        collection = db["commissions"]
        update_data = data.copy()
        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one(
            {"_id": ObjectId(id), "scheme_id": scheme_id},
            {"$set": update_data}
        )
        return {"status": "success" if result.modified_count else "not updated"}

    @staticmethod
    async def get_all_commissions(scheme_id: str = None):
        collection = db["commissions"]
        query = {}
        if scheme_id:
            query["scheme_id"] = scheme_id
        cursor = collection.find(query)
        commissions = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            commissions.append(CommissionBase(**doc))
        return commissions


    
    
