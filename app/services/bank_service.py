from app.db.mongo import db
from bson import ObjectId
from datetime import datetime
from app.models.bank_model import BankCreate, BankUpdate, BankBase

class BankService:
    @staticmethod
    async def create_bank(data: BankCreate):
        collection = db["fundbanks"]
        now = datetime.utcnow()
        new_data = data.dict()
        new_data.update({"created_at": now, "updated_at": now})

        result = await collection.insert_one(new_data)
        return {"status": "success", "id": str(result.inserted_id)}

    @staticmethod
    async def get_all_banks():
        collection = db["fundbanks"]
        cursor = collection.find()
        banks = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            banks.append(BankBase(**doc))
        return banks

    @staticmethod
    async def update_bank(data: BankUpdate):
        collection = db["fundbanks"]
        update_data = data.dict()
        update_data.pop("id")
        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one({"_id": ObjectId(data.id)}, {"$set": update_data})
        if result.modified_count:
            return {"status": "success"}
        return {"status": "not updated"}

    @staticmethod
    async def delete_bank(id: str):
        collection = db["fundbanks"]
        result = await collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"status": "success"}
        return {"status": "not deleted"}
